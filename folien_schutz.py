"""Passwortgeschützte Foliensätze für die Kursseite (ohne Backend).

Die Foliensätze liegen im Klartext nur lokal im Lehrerordner. Beim Bauen werden sie
komprimiert und verschlüsselt (PBKDF2-SHA256 -> AES-256-CTR + HMAC-SHA256); online liegt
nur der verschlüsselte Text. Der Browser entschlüsselt mit WebCrypto nach Passworteingabe.

Einstellungen (NICHT im Repo): _Lehrer/_werkzeuge/webseite/folien.json
  {"passwort": "…", "ordner": "…", "saetze": [{"titel": "…", "datei": "LB7_…/folien/….html"}]}
"""
import base64
import hashlib
import hmac
import html
import json
import mimetypes
import os
import re
import secrets
import zlib

ITERATIONEN = 600_000

# ---------------------------------------------------------------- AES (nur Verschlüsseln, für CTR)
def _sbox():
    s = [0] * 256
    p = q = 1
    while True:
        p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)
        q ^= q << 1
        q ^= q << 2
        q ^= q << 4
        q &= 0xFF
        if q & 0x80:
            q ^= 0x09
        x = q ^ ((q << 1 | q >> 7) & 0xFF) ^ ((q << 2 | q >> 6) & 0xFF) ^ ((q << 3 | q >> 5) & 0xFF) ^ ((q << 4 | q >> 4) & 0xFF)
        s[p] = x ^ 0x63
        if p == 1:
            break
    s[0] = 0x63
    return s


SBOX = _sbox()


def _xt(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else a << 1


T0 = []
for _s in SBOX:
    T0.append((_xt(_s) << 24) | (_s << 16) | (_s << 8) | (_xt(_s) ^ _s))
T1 = [((t >> 8) | (t << 24)) & 0xFFFFFFFF for t in T0]
T2 = [((t >> 16) | (t << 16)) & 0xFFFFFFFF for t in T0]
T3 = [((t >> 24) | (t << 8)) & 0xFFFFFFFF for t in T0]


def _schluesselplan(key):
    nk = len(key) // 4
    w = [int.from_bytes(key[4 * i:4 * i + 4], "big") for i in range(nk)]
    rcon = 1
    for i in range(nk, 4 * (nk + 7)):
        t = w[i - 1]
        if i % nk == 0:
            t = ((t << 8) | (t >> 24)) & 0xFFFFFFFF
            t = (SBOX[t >> 24] << 24) | (SBOX[(t >> 16) & 255] << 16) | (SBOX[(t >> 8) & 255] << 8) | SBOX[t & 255]
            t ^= rcon << 24
            rcon = _xt(rcon)
        elif nk > 6 and i % nk == 4:
            t = (SBOX[t >> 24] << 24) | (SBOX[(t >> 16) & 255] << 16) | (SBOX[(t >> 8) & 255] << 8) | SBOX[t & 255]
        w.append(w[i - nk] ^ t)
    return w


def _block(w, b):
    s0 = int.from_bytes(b[0:4], "big") ^ w[0]
    s1 = int.from_bytes(b[4:8], "big") ^ w[1]
    s2 = int.from_bytes(b[8:12], "big") ^ w[2]
    s3 = int.from_bytes(b[12:16], "big") ^ w[3]
    runden = len(w) // 4 - 1
    k = 4
    for _ in range(runden - 1):
        t0 = T0[s0 >> 24] ^ T1[(s1 >> 16) & 255] ^ T2[(s2 >> 8) & 255] ^ T3[s3 & 255] ^ w[k]
        t1 = T0[s1 >> 24] ^ T1[(s2 >> 16) & 255] ^ T2[(s3 >> 8) & 255] ^ T3[s0 & 255] ^ w[k + 1]
        t2 = T0[s2 >> 24] ^ T1[(s3 >> 16) & 255] ^ T2[(s0 >> 8) & 255] ^ T3[s1 & 255] ^ w[k + 2]
        t3 = T0[s3 >> 24] ^ T1[(s0 >> 16) & 255] ^ T2[(s1 >> 8) & 255] ^ T3[s2 & 255] ^ w[k + 3]
        s0, s1, s2, s3 = t0, t1, t2, t3
        k += 4
    S = SBOX
    o = bytearray(16)
    for i, (a, bb, c, d) in enumerate(((s0, s1, s2, s3), (s1, s2, s3, s0), (s2, s3, s0, s1), (s3, s0, s1, s2))):
        x = ((S[a >> 24] << 24) | (S[(bb >> 16) & 255] << 16) | (S[(c >> 8) & 255] << 8) | S[d & 255]) ^ w[k + i]
        o[4 * i:4 * i + 4] = x.to_bytes(4, "big")
    return bytes(o)


def aes_ctr(key, iv, daten):
    """AES-CTR wie WebCrypto (Zähler = ganze 16 Byte, length 64: untere 64 Bit zählen hoch)."""
    w = _schluesselplan(key)
    vorne = iv[:8]
    zaehler = int.from_bytes(iv[8:], "big")
    strom = bytearray()
    for _ in range((len(daten) + 15) // 16):
        strom += _block(w, vorne + zaehler.to_bytes(8, "big"))
        zaehler = (zaehler + 1) & 0xFFFFFFFFFFFFFFFF
    n = len(daten)
    return (int.from_bytes(daten, "big") ^ int.from_bytes(bytes(strom[:n]), "big")).to_bytes(n, "big")


# ---------------------------------------------------------------- Foliensatz vorbereiten
def bilder_einbetten(text, ordner):
    """bilder/x.jpg -> data:-URI, damit der Foliensatz eine einzige Datei ist."""
    def ersetze(m):
        pfad = os.path.join(ordner, m.group(0))
        if not os.path.isfile(pfad):
            return m.group(0)
        typ = mimetypes.guess_type(pfad)[0] or "application/octet-stream"
        with open(pfad, "rb") as f:
            return f"data:{typ};base64," + base64.b64encode(f.read()).decode()
    text = re.sub(r"bilder/[A-Za-z0-9_.-]+\.(?:jpe?g|png|gif|svg|webp)", ersetze, text)

    # danebenliegende CSS-/JS-Dateien (z. B. LB1 folien.html) direkt einsetzen
    def css(m):
        p = os.path.join(ordner, m.group(1))
        return f"<style>{open(p, encoding='utf-8').read()}</style>" if os.path.isfile(p) else m.group(0)

    def js(m):
        p = os.path.join(ordner, m.group(1))
        return f"<script>{open(p, encoding='utf-8').read()}</script>" if os.path.isfile(p) else m.group(0)
    text = re.sub(r'<link rel="stylesheet" href="([A-Za-z0-9_.-]+\.css)">', css, text)
    return re.sub(r'<script src="([A-Za-z0-9_.-]+\.js)"></script>', js, text)


def verschluesseln(klartext, schluessel):
    iv = secrets.token_bytes(16)
    iv = iv[:8] + bytes(8)  # Zähler beginnt bei 0
    ct = aes_ctr(schluessel[:32], iv, zlib.compress(klartext.encode("utf-8"), 9))
    mac = hmac.new(schluessel[32:], iv + ct, hashlib.sha256).digest()
    return iv, ct, mac


def b64(x):
    return base64.b64encode(x).decode()


SEITE = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{titel}</title>
<style>
body{{font-family:system-ui,sans-serif;background:#f4f5f7;color:#1c2330;display:grid;place-items:center;min-height:100vh;margin:0}}
form{{background:#fff;padding:28px 32px;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,.08);width:min(360px,90vw)}}
h1{{font-size:1.15rem;margin:0 0 16px}} input[type=password]{{width:100%;box-sizing:border-box;padding:10px;font-size:1rem;border:1px solid #c5cad3;border-radius:8px}}
label{{display:flex;gap:8px;align-items:center;margin:12px 0;font-size:.9rem;color:#4a5363}}
button{{padding:10px 16px;font-size:1rem;border:0;border-radius:8px;background:#1d4ed8;color:#fff;cursor:pointer;width:100%}}
#meldung{{color:#b42318;font-size:.9rem;min-height:1.2em;margin:10px 0 0}} ul{{padding-left:1.2em;line-height:1.8}} a{{color:#1d4ed8}}
@media (prefers-color-scheme:dark){{body{{background:#14181f;color:#e6e9ef}}form{{background:#1d232d}}input[type=password]{{background:#14181f;color:#e6e9ef;border-color:#3a4352}}label{{color:#a9b1bf}}a{{color:#8fb0ff}}}}
</style></head><body>
<form id="f" hidden><h1>{titel}</h1>
<input type="password" id="pw" placeholder="Passwort" autocomplete="current-password" autofocus>
<label><input type="checkbox" id="merken"> auf diesem Gerät merken</label>
<button>Öffnen</button><p id="meldung"></p></form>
<script>
const D={daten};
const b=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const s64=a=>btoa(String.fromCharCode(...new Uint8Array(a)));
const KEY='folien-schluessel';
function gemerkt(){{for(const st of [sessionStorage,localStorage]){{try{{const v=JSON.parse(st.getItem(KEY)||'null');if(v&&v.salt===D.salt)return b(v.bits)}}catch(e){{}}}}return null}}
async function ableiten(pw){{const k=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveBits']);
return new Uint8Array(await crypto.subtle.deriveBits({{name:'PBKDF2',salt:b(D.salt),iterations:D.iter,hash:'SHA-256'}},k,512))}}
async function oeffnen(bits){{const mk=await crypto.subtle.importKey('raw',bits.slice(32),{{name:'HMAC',hash:'SHA-256'}},false,['verify']);
const iv=b(D.iv),ct=b(D.ct),daten=new Uint8Array(iv.length+ct.length);daten.set(iv);daten.set(ct,iv.length);
if(!await crypto.subtle.verify('HMAC',mk,b(D.mac),daten))return null;
const ak=await crypto.subtle.importKey('raw',bits.slice(0,32),'AES-CTR',false,['decrypt']);
const pt=await crypto.subtle.decrypt({{name:'AES-CTR',counter:iv,length:64}},ak,ct);
return await new Response(new Blob([pt]).stream().pipeThrough(new DecompressionStream('deflate'))).text()}}
function zeigen(text){{document.open();document.write(text);document.close()}}
(async()=>{{const g=gemerkt();if(g){{const t=await oeffnen(g);if(t)return zeigen(t)}}
const f=document.getElementById('f');f.hidden=false;document.getElementById('pw').focus();
f.onsubmit=async ev=>{{ev.preventDefault();const m=document.getElementById('meldung');m.textContent='Entschlüssele …';
const bits=await ableiten(document.getElementById('pw').value);const t=await oeffnen(bits);
if(!t){{m.textContent='Passwort falsch.';return}}
const wert=JSON.stringify({{salt:D.salt,bits:s64(bits)}});
try{{sessionStorage.setItem(KEY,wert);if(document.getElementById('merken').checked)localStorage.setItem(KEY,wert)}}catch(e){{}}
zeigen(t)}}}})();
</script></body></html>
"""

UEBERSICHT = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Foliensätze</title>
<style>body{{font-family:system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 16px;line-height:1.8;color:#1c2330}}
a{{color:#1d4ed8}} button{{font:inherit;font-size:.85rem;margin-top:20px}}
@media (prefers-color-scheme:dark){{body{{background:#14181f;color:#e6e9ef}}a{{color:#8fb0ff}}}}</style></head><body>
<h1>Foliensätze</h1>
<ul>
{liste}
</ul>
<button onclick="try{{localStorage.removeItem('folien-schluessel');sessionStorage.removeItem('folien-schluessel')}}catch(e){{}};this.textContent='Gemerktes Passwort gelöscht'">Gemerktes Passwort auf diesem Gerät löschen</button>
</body></html>
"""


def folien_bauen(einstellungen_pfad, lehrer_ordner, site):
    """Verschlüsselte Foliensätze nach <site>/<ordner>/ schreiben. Gibt die Anzahl zurück."""
    with open(einstellungen_pfad, encoding="utf-8") as f:
        cfg = json.load(f)
    pw = cfg["passwort"]
    # Salz aus dem Passwort abgeleitet: gleich bleibend, solange das Passwort gleich bleibt
    # (gemerkte Schlüssel gelten weiter), neu, sobald es geändert wird.
    salt = hashlib.sha256(("lk-informatik-folien|" + pw).encode()).digest()[:16]
    schluessel = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, ITERATIONEN, 64)
    ziel = os.path.join(site, cfg["ordner"])
    os.makedirs(ziel, exist_ok=True)
    zeilen = []
    for satz in cfg["saetze"]:
        quelle = os.path.join(lehrer_ordner, satz["datei"])
        with open(quelle, encoding="utf-8") as f:
            text = bilder_einbetten(f.read(), os.path.dirname(quelle))
        iv, ct, mac = verschluesseln(text, schluessel)
        name = os.path.splitext(os.path.basename(quelle))[0] + ".html"
        daten = json.dumps({"salt": b64(salt), "iter": ITERATIONEN, "iv": b64(iv), "ct": b64(ct), "mac": b64(mac)})
        with open(os.path.join(ziel, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(SEITE.format(titel=html.escape(satz["titel"]), daten=daten))
        zeilen.append(f'<li><a href="{name}">{html.escape(satz["titel"])}</a></li>')
    with open(os.path.join(ziel, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(UEBERSICHT.format(liste="\n".join(zeilen)))
    return len(cfg["saetze"])

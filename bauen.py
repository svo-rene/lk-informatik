"""Baut die Kurswebseite aus `inhalt/` nach `_site/`.

    python bauen.py            # baut _site/
    python bauen.py --zeigen   # baut und startet http://localhost:8000

Aufbau von inhalt/:
    kurs.json                         Titel, Reihenfolge der Lernbereiche, Bildnachweise
    <lernbereich>/bereich.json        Nummer, Titel, Kurztext, Kapitel mit Themen (Ordnernamen)
    <lernbereich>/<thema>/thema.json  Nummer, Titel, Liste der Unterseiten
    <lernbereich>/<thema>/index.html  Einführung (nur der Seiteninhalt, ohne <html>/<head>)
    <lernbereich>/<thema>/uebungen.html, vertiefung.html, weitere Zusatzseiten
    <lernbereich>/img, vid, material, notebooks   Dateien, verlinkt als ../img/… usw.
"""
import html
import json
import re
import os
import shutil
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
INHALT = os.path.join(HIER, "inhalt")
VORLAGE = os.path.join(HIER, "vorlage")
SITE = os.path.join(HIER, "_site")


def lies_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def schreibe(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def e(s):
    return html.escape(s, quote=True)


SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
SVG_LUPE = SVG.format('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>')
SVG_MENUE = SVG.format('<path d="M4 6h16M4 12h16M4 18h16"/>')
SVG_MOND = SVG.format('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>')
SVG_SONNE = SVG.format('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>')


# ---------------------------------------------------------------------------
def laden():
    kurs = lies_json(os.path.join(INHALT, "kurs.json"))
    bereiche = []
    for slug in kurs["bereiche"]:
        b = lies_json(os.path.join(INHALT, slug, "bereich.json"))
        b["slug"] = slug
        b["alle_themen"] = []
        for k in b["kapitel"]:
            themen = []
            for t in k["themen"]:
                m = lies_json(os.path.join(INHALT, slug, t, "thema.json"))
                m["slug"] = t
                m["bereich"] = b
                themen.append(m)
                b["alle_themen"].append(m)
            k["themen_meta"] = themen
        bereiche.append(b)
    return kurs, bereiche


def themenname(t):
    return (t["nr"] + " " if t["nr"] else "") + t["titel"]


# ---------------------------------------------------------------------------
def seitenleiste(bereiche, root, aktiv_bereich=None, aktiv_thema=None):
    z = ['<nav class="leiste" id="leiste" aria-label="Lernbereiche">',
         '<div class="suche">' + SVG_LUPE + '<input type="search" id="filter" placeholder="Thema suchen …" aria-label="Thema suchen"></div>',
         f'<a class="leiste-start{" aktiv" if aktiv_bereich is None else ""}" href="{root}index.html">Überblick</a>']
    for b in bereiche:
        offen = " open" if aktiv_bereich is b else ""
        z.append(f'<details class="lb"{offen}><summary><span class="lb-nr">{e(b["nr"])}</span> {e(b["titel"])}</summary>'
                 '<div class="lb-inhalt">')
        z.append(f'<a class="lb-uebersicht{" aktiv" if aktiv_bereich is b and aktiv_thema is None else ""}" '
                 f'href="{root}{b["slug"]}/index.html">Überblick {e(b["titel"])}</a>')
        for k in b["kapitel"]:
            z.append(f'<p class="kap">{e(k["titel"])}</p><ul>')
            for t in k["themen_meta"]:
                cls = ' class="aktiv" aria-current="page"' if t is aktiv_thema else ""
                z.append(f'<li><a{cls} href="{root}{b["slug"]}/{t["slug"]}/index.html">'
                         f'<span class="t-nr">{e(t["nr"])}</span> {e(t["titel"])}</a></li>')
            z.append("</ul>")
        z.append("</div></details>")
    z.append("</nav>")
    return "\n".join(z)


def geruest(kurs, bereiche, root, titel, inhalt, aktiv_bereich=None, aktiv_thema=None, toc=False):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel) if titel == kurs["titel"] else e(titel) + " – " + e(kurs["titel"])}</title>
<script>try{{var t=localStorage.getItem("thema");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}assets/inhalt.css">
<link rel="stylesheet" href="{root}assets/seite.css">
<link rel="icon" href="{root}assets/icon.svg" type="image/svg+xml">
</head>
<body class="{"mit-toc" if toc else ""}" data-root="{root}">
<header class="kopf">
  <button class="menue-knopf" id="menue-knopf" aria-controls="leiste" aria-expanded="false">{SVG_MENUE}<span>Themen</span></button>
  <a class="marke" href="{root}index.html"><span class="marke-zeichen">&lt;/&gt;</span><span>{e(kurs["titel"])}</span></a>
  <div class="kopf-rechts">
    <button class="knopf-rund" id="thema-knopf" title="Hell oder dunkel" aria-label="Hell oder dunkel umschalten">
      <span class="thema-dunkel">{SVG_MOND}</span><span class="thema-hell">{SVG_SONNE}</span>
    </button>
  </div>
</header>
<div class="rahmen">
{seitenleiste(bereiche, root, aktiv_bereich, aktiv_thema)}
<div class="haupt-rahmen">
<main class="haupt" id="inhalt">
{inhalt}
</main>
{'<aside class="toc" id="toc" aria-label="Auf dieser Seite"></aside>' if toc else ""}
</div>
</div>
<footer class="fuss">
  <a href="{root}hinweise.html">Hinweise und Bildnachweise</a>
  <a href="{root}impressum.html">Impressum</a>
</footer>
<script src="{root}assets/prism.js"></script>
<script src="{root}assets/seite.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
def startseite(kurs, bereiche):
    karten = []
    for b in bereiche:
        n = len(b["alle_themen"])
        karten.append(f"""<a class="karte" href="{b["slug"]}/index.html">
  <span class="karte-nr">{e(b["nr"])}</span>
  <span class="karte-titel">{e(b["titel"])}</span>
  <span class="karte-text">{e(b["text"])}</span>
  <span class="karte-fuss">{n} Themen</span>
</a>""")
    inhalt = f"""
<section class="held">
  <h1>{e(kurs["titel"])}</h1>
  <p class="unterzeile">Alle Themen des Kurses an einem Ort – zum Nachlesen, Üben und Vertiefen.</p>
</section>

<h2>So ist jedes Thema aufgebaut</h2>
<div class="aufbau">
  <div class="aufbau-teil"><span class="aufbau-kopf"><span class="aufbau-zahl">1</span>Einführung</span>
    <p>Worum es geht, Beispiele und Erklärvideos. Am Ende <strong>Das Wichtigste</strong> zum Merken und ein bis zwei <strong>Grundaufgaben</strong>.</p></div>
  <div class="aufbau-teil"><span class="aufbau-kopf"><span class="aufbau-zahl">2</span>Übungen</span>
    <p>Weitere Aufgaben aus dem Unterricht und zum Üben zu Hause, dazu Notebooks und Material zum Herunterladen.</p></div>
  <div class="aufbau-teil"><span class="aufbau-kopf"><span class="aufbau-zahl">3</span>Vertiefung</span>
    <p>Anspruchsvollere Aufgaben, Lösungswege und interaktive Werkzeuge für alle, die weiter gehen wollen.</p></div>
</div>

<h2>Lernbereiche</h2>
<div class="karten">
{"".join(karten)}
</div>
"""
    return geruest(kurs, bereiche, "", kurs["titel"], inhalt)


def bereichseite(kurs, bereiche, b):
    root = "../"
    teile = [f'<p class="pfad"><a href="{root}index.html">Überblick</a> › {e(b["nr"])}</p>',
             f'<h1><span class="h1-nr">{e(b["nr"])}</span> {e(b["titel"])}</h1>',
             f'<p class="unterzeile">{e(b["text"])}</p>']
    for k in b["kapitel"]:
        teile.append(f'<h2>{e(k["titel"])}</h2><ul class="themenliste">')
        for t in k["themen_meta"]:
            marken = "".join(f'<span class="marke-klein m-{"zusatz" if s.get("zusatz") else s["datei"][:-5]}">{e(s["titel"])}</span>'
                             for s in t["seiten"][1:])
            teile.append(f'<li><a href="{t["slug"]}/index.html"><span class="t-nr">{e(t["nr"])}</span> {e(t["titel"])}</a>{marken}</li>')
        teile.append("</ul>")
    return geruest(kurs, bereiche, root, f'{b["nr"]} {b["titel"]}', "\n".join(teile), aktiv_bereich=b)


def rechnung_html(text):
    """Schriftliche Rechnung aus <pre class="rechnung"> als Kästchen-Tabelle.

    Je Zeile:  Beschriftung | … | Zahl  # Notiz   (# mit Leerzeichen davor und danach)
    - Das letzte Feld vor # ist die Zahl: ohne Leerzeichen ein Kästchen je Zeichen (0,0625),
      mit Leerzeichen ein Kästchen je Stück (0 1 1 0, auch (1) für einen Überlauf). "." = leeres Kästchen.
    - Alle Zahlen stehen rechtsbündig, Kommazahlen am Komma ausgerichtet.
    - Eine Zeile nur aus - oder — zieht den Ergebnisstrich über der nächsten Zeile.
    - Beginnt die Beschriftung mit "Übertrag", wird die Zeile klein gesetzt.
    Beschriftung und Notiz dürfen HTML enthalten (C<sub>in</sub>).
    """
    zeilen = []
    strich = False
    for z in text.strip("\n").split("\n"):
        if not z.strip():
            continue
        if re.fullmatch(r"\s*(-|—|&mdash;)+\s*", z):
            strich = True
            continue
        notiz = ""
        if re.search(r"\s#\s", z):
            z, notiz = re.split(r"\s#\s", z, maxsplit=1)
        teile = [p.strip() for p in z.split("|")]
        zahl = html.unescape(teile[-1])
        stuecke = zahl.split() if " " in zahl else list(zahl)
        if "," in stuecke:
            k = stuecke.index(",")
            ganz, bruch, komma = stuecke[:k], stuecke[k + 1:], True
        else:
            ganz, bruch, komma = stuecke, [], False
        art = "ergebnis" if strich else ("uebertrag" if teile[0].startswith("Übertrag") else "")
        zeilen.append({"marken": teile[:-1], "ganz": ganz, "bruch": bruch, "komma": komma,
                       "notiz": notiz.strip(), "art": art})
        strich = False
    if not zeilen:
        return ""
    n_marken = max(len(z["marken"]) for z in zeilen)
    n_ganz = max(len(z["ganz"]) for z in zeilen)
    n_bruch = max(len(z["bruch"]) for z in zeilen)
    mit_komma = any(z["komma"] for z in zeilen)
    mit_notiz = any(z["notiz"] for z in zeilen)

    def kaestchen(s, extra=""):
        klasse = extra
        if s == ".":
            s = ""
        elif s.startswith("("):
            klasse = (klasse + " ueberlauf").strip()
        k = f' class="{klasse}"' if klasse else ""
        return f"<td{k}>{e(s)}</td>"

    reihen = []
    for z in zeilen:
        marken = z["marken"] + [""] * (n_marken - len(z["marken"]))
        zellen = "".join(f'<th scope="row">{m}</th>' for m in marken)
        zellen += "".join(kaestchen(s) for s in [""] * (n_ganz - len(z["ganz"])) + z["ganz"])
        if mit_komma:
            zellen += kaestchen("," if z["komma"] else "", "komma")
        zellen += "".join(kaestchen(s) for s in z["bruch"] + [""] * (n_bruch - len(z["bruch"])))
        if mit_notiz:
            zellen += f'<td class="notiz">{z["notiz"]}</td>'
        k = f' class="{z["art"]}"' if z["art"] else ""
        reihen.append(f"<tr{k}>{zellen}</tr>")
    return '<div class="rechnung-rahmen"><table class="rechnung">' + "".join(reihen) + "</table></div>"


def rechnungen(roh):
    return re.sub(r'<pre class="rechnung">(.*?)</pre>', lambda m: rechnung_html(m.group(1)), roh, flags=re.S)


def themenseite(kurs, bereiche, b, t, seite, vorher, nachher):
    root = "../../"
    pfad = os.path.join(INHALT, b["slug"], t["slug"], seite["datei"])
    roh = rechnungen(lies(pfad))
    reiter = []
    for s in t["seiten"]:
        aktiv = ' class="aktiv" aria-current="page"' if s is seite else ""
        z = ' <span class="zusatz-marke">interaktiv</span>' if s.get("zusatz") else ""
        anz = len(re.findall(r"<summary[^>]*>\s*Aufgabe\b", lies(os.path.join(INHALT, b["slug"], t["slug"], s["datei"]))))
        zahl = f' <span class="r-zahl">{anz}</span>' if anz and not s.get("zusatz") else ""
        reiter.append(f'<a{aktiv} href="{s["datei"]}">{e(s["titel"])}{zahl}{z}</a>')
    weiter = ""
    if seite["datei"] == "index.html" and len(t["seiten"]) > 1:
        links = "".join(f'<a class="weiter-link" href="{s["datei"]}">{e(s["titel"])} →</a>' for s in t["seiten"][1:])
        weiter = f'<div class="weiter-kasten"><p><strong>Weiter mit diesem Thema</strong></p>{links}</div>'
    nav = '<nav class="blaettern" aria-label="Themen blättern">'
    nav += (f'<a class="zurueck" href="../{vorher["slug"]}/index.html"><small>← Vorheriges Thema</small>{e(themenname(vorher))}</a>' if vorher else "")
    nav += (f'<a class="vor" href="../{nachher["slug"]}/index.html"><small>Nächstes Thema →</small>{e(themenname(nachher))}</a>' if nachher else "")
    nav += "</nav>"
    unterseite = "" if seite["datei"] == "index.html" else f' › {e(seite["titel"])}'
    inhalt = f"""<p class="pfad"><a href="{root}index.html">Überblick</a> › <a href="../index.html">{e(b["nr"])} {e(b["titel"])}</a>{unterseite}</p>
<h1><span class="h1-nr">{e(t["nr"])}</span> {e(t["titel"])}</h1>
<nav class="reiter" aria-label="Teile dieses Themas">{"".join(reiter)}</nav>
<div class="seiteninhalt{" immer-hell" if seite.get("zusatz") else ""}">
{roh}
</div>
{weiter}
{nav}"""
    titel = themenname(t) + ("" if seite["datei"] == "index.html" else " – " + seite["titel"])
    return geruest(kurs, bereiche, root, titel, inhalt, aktiv_bereich=b, aktiv_thema=t, toc=True)


def hinweisseite(kurs, bereiche):
    zeilen = "".join(f'<tr><td><code>{e(n["datei"])}</code></td><td>{e(n["urheber"])}</td><td>{e(n["lizenz"])}</td></tr>'
                     for n in kurs.get("nachweise", []))
    inhalt = f"""<h1>Hinweise, Lizenzen und Bildnachweise</h1>
<p>Diese Seite enthält Unterrichtsmaterial für den Leistungskurs Informatik. Texte, Aufgaben, Grafiken, Videos und Programme
sind – soweit unten nicht anders angegeben – selbst erstellt.</p>
<h2>Fremdmaterial mit freier Lizenz</h2>
<table><thead><tr><th>Datei</th><th>Urheber</th><th>Lizenz</th></tr></thead><tbody>{zeilen}</tbody></table>
<p>Bildschirmfotos zeigen die Programme Filius, Thonny, Forgejo, DB Browser for SQLite, LibreOffice und schulKI bei der Benutzung.</p>
<h2>Python im Browser</h2>
<p>Programme mit dem Knopf „Ausführen“ laufen mit <a href="https://natter.wi7.net/">Natter</a> (Julian Dorn, MIT-Lizenz) direkt im Browser.
Natter wird erst beim ersten Klick über jsDelivr geladen; dabei überträgt der Browser seine IP-Adresse an jsDelivr.</p>
<h2>Verlinkte Angebote</h2>
<p>Links zu anderen Webseiten (z.&nbsp;B. Jupyter, FLACI, inf-schule) führen zu Angeboten Dritter. Für deren Inhalte sind die jeweiligen Anbieter verantwortlich.</p>
"""
    return geruest(kurs, bereiche, "", "Hinweise", inhalt)


def impressumseite(kurs, bereiche):
    inhalt = """<h1>Impressum</h1>
<div class="hinweis"><p>Diese Seite wird noch ergänzt.</p></div>
<h2>Angaben</h2>
<p>[Name]<br>[Anschrift]</p>
<h2>Kontakt</h2>
<p>[E-Mail-Adresse]</p>
<h2>Verantwortlich für den Inhalt</h2>
<p>[Name, Anschrift]</p>
<h2>Datenschutz</h2>
<p>[Hinweise zum Hosting bei GitHub Pages und zu eingebundenen Diensten]</p>
"""
    return geruest(kurs, bereiche, "", "Impressum", inhalt)


# ---------------------------------------------------------------------------
def bauen():
    kurs, bereiche = laden()
    if os.path.isdir(SITE):
        def schreibbar(fn, pfad, _):  # git legt schreibgeschützte Dateien an
            os.chmod(pfad, 0o666)
            fn(pfad)
        shutil.rmtree(SITE, onexc=schreibbar)
    os.makedirs(SITE)
    shutil.copytree(VORLAGE, os.path.join(SITE, "assets"))
    schreibe(os.path.join(SITE, ".nojekyll"), "")
    schreibe(os.path.join(SITE, "index.html"), startseite(kurs, bereiche))
    schreibe(os.path.join(SITE, "hinweise.html"), hinweisseite(kurs, bereiche))
    schreibe(os.path.join(SITE, "impressum.html"), impressumseite(kurs, bereiche))
    anzahl = 3
    for b in bereiche:
        quelle = os.path.join(INHALT, b["slug"])
        ziel = os.path.join(SITE, b["slug"])
        themen = {t["slug"] for t in b["alle_themen"]}
        # Dateien des Lernbereichs (img, vid, material, notebooks, Skripte) unverändert kopieren
        for x in os.listdir(quelle):
            p = os.path.join(quelle, x)
            if x in themen or x == "bereich.json":
                continue
            if os.path.isdir(p):
                shutil.copytree(p, os.path.join(ziel, x))
            else:
                os.makedirs(ziel, exist_ok=True)
                shutil.copy2(p, os.path.join(ziel, x))
        schreibe(os.path.join(ziel, "index.html"), bereichseite(kurs, bereiche, b))
        anzahl += 1
        liste = b["alle_themen"]
        for i, t in enumerate(liste):
            vorher = liste[i - 1] if i > 0 else None
            nachher = liste[i + 1] if i + 1 < len(liste) else None
            for s in t["seiten"]:
                schreibe(os.path.join(ziel, t["slug"], s["datei"]), themenseite(kurs, bereiche, b, t, s, vorher, nachher))
                anzahl += 1
    print(f"{anzahl} Seiten nach {SITE} geschrieben.")


def veroeffentlichen():
    """_site als eigenen Commit in den Branch gh-pages schieben (GitHub Pages: Branch gh-pages, Ordner /)."""
    import subprocess
    remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=HIER, capture_output=True, text=True,
                            check=True).stdout.strip()
    name = subprocess.run(["git", "config", "user.name"], cwd=HIER, capture_output=True, text=True).stdout.strip()
    mail = subprocess.run(["git", "config", "user.email"], cwd=HIER, capture_output=True, text=True).stdout.strip()
    stand = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=HIER, capture_output=True, text=True).stdout.strip()

    def git(*args):
        subprocess.run(["git", "-c", f"user.name={name}", "-c", f"user.email={mail}", *args], cwd=SITE, check=True)
    git("init", "-q", "-b", "gh-pages")
    git("add", "-A")
    git("commit", "-q", "-m", f"Seite gebaut aus {stand}")
    git("push", "-q", "--force", remote, "gh-pages")
    bauen()  # _site ohne .git neu schreiben
    print("Veröffentlicht. GitHub Pages braucht danach etwa eine Minute.")


if __name__ == "__main__":
    bauen()
    if "--veroeffentlichen" in sys.argv:
        veroeffentlichen()
    if "--zeigen" in sys.argv:
        import http.server
        import functools
        h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
        print("http://localhost:8000  (Strg+C beendet)")
        http.server.ThreadingHTTPServer(("localhost", 8000), h).serve_forever()

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
import hashlib
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
         f'<a class="leiste-start{" aktiv" if aktiv_bereich is None else ""}" href="{root}index.html">Überblick</a>',
         f'<a class="leiste-start{" aktiv" if aktiv_bereich == "werkzeuge" else ""}" href="{root}werkzeuge.html">Werkzeuge</a>',
         f'<a class="leiste-start{" aktiv" if aktiv_bereich == "projekte" else ""}" href="{root}projekte.html">Lernprojekte</a>']
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
<script>try{{var t=localStorage.getItem("thema");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}if(/[?&]vollseite/.test(location.search))document.documentElement.classList.add("vollseite")</script>
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
# Werkzeugseite: füllt sich beim Bauen von selbst aus den Inhalten
#  - interaktive Zusatzseiten (thema.json: "zusatz": true, optional "beschreibung")
#  - Sortierlabor (<div class="sortierlabor" data-verfahren="…">)
#  - eingebettete Übungen von LearningApps und H5P (<iframe>)
#  - Lernspiele aus kurs.json ("lernspiele")
VERFAHREN = {"bubble": "Bubblesort", "insertion": "Insertionsort", "selection": "Selectionsort",
             "merge": "Mergesort", "mergeteil": "Mergesort", "quick": "Quicksort", "quickinplace": "Quicksort",
             "rennen": "Verfahren im Rennen vergleichen", "hochrechner": "Laufzeit hochrechnen"}


def _klartext(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _titel_davor(s, pos):
    """Titel der Aufgabe, in der eine eingebettete Übung steckt (leer, wenn sie frei auf der Seite steht)."""
    kandidaten = list(re.finditer(r"<summary[^>]*>(.*?)</summary>", s[:pos], re.S))
    if not kandidaten or "</details>" in s[kandidaten[-1].end():pos]:
        return ""
    t = _klartext(kandidaten[-1].group(1))
    t = re.sub(r"\s*(AFB\s*[I/]+.*|einfach|komplex)$", "", t)
    t = re.sub(r"^(Aufgabe|Beispiel)\s*[\d.]*\s*:?\s*", "", t)
    return re.sub(r"\s*\((LearningApps|H5P)\)\s*$", "", t).strip()


def werkzeuge_sammeln(bereiche):
    je_bereich = []
    for b in bereiche:
        liste = []
        for t in b["alle_themen"]:
            for s in t["seiten"]:
                pfad = os.path.join(INHALT, b["slug"], t["slug"], s["datei"])
                roh = lies(pfad)
                link = f'{b["slug"]}/{t["slug"]}/{s["datei"]}'
                thema = f'{t["nr"]} {t["titel"]}'
                if s.get("zusatz"):
                    text = s.get("beschreibung")
                    if not text:
                        m = re.search(r"<p[^>]*>(.*?)</p>", roh, re.S)
                        text = _klartext(m.group(1)) if m else ""
                        if len(text) > 200:
                            text = text[:200].rsplit(" ", 1)[0] + " …"
                    art = "Übung" if "übung" in s["titel"].lower() else "Simulation"
                    liste.append({"art": art, "titel": s["titel"], "text": text, "link": link, "thema": thema})
                verfahren = []
                for v in re.findall(r'class="sortierlabor"[^>]*data-verfahren="([^"]+)"', roh):
                    for x in v.split(","):
                        name = VERFAHREN.get(x.strip(), x.strip())
                        if name not in verfahren:
                            verfahren.append(name)
                if verfahren:
                    liste.append({"art": "Labor", "titel": "Sortierlabor",
                                  "text": "Sortieren Schritt für Schritt ausprobieren und Vergleiche zählen. Auf dieser Seite: " + ", ".join(verfahren) + ".",
                                  "link": link, "thema": thema + " · " + s["titel"]})
                for m in re.finditer(r'<iframe[^>]*src="([^"]+)"', roh):
                    src = m.group(1)
                    if "learningapps.org" in src:
                        quelle = "LearningApps"
                    elif "/h5p/" in src:
                        quelle = "H5P"
                    else:
                        continue  # Videos u. Ä. sind keine Werkzeuge
                    titel = _titel_davor(roh, m.start()) or f'Übung zu „{t["titel"]}“'
                    liste.append({"art": "Übung", "titel": titel, "text": f"Interaktive Übung ({quelle}) direkt auf der Seite.",
                                  "link": link, "thema": thema + " · " + s["titel"]})
        if liste:
            je_bereich.append((b, liste))
    return je_bereich


def werkzeugseite(kurs, bereiche):
    teile = ['<p class="pfad"><a href="index.html">Überblick</a> › Werkzeuge</p>',
             "<h1>Werkzeuge</h1>",
             '<p class="unterzeile">Simulationen, Labore und interaktive Übungen aus allen Themen an einem Ort. '
             "Die Liste füllt sich von selbst, sobald ein Thema ein neues interaktives Werkzeug bekommt.</p>"]
    for b, liste in werkzeuge_sammeln(bereiche):
        teile.append(f'<h2 id="{b["slug"]}"><span class="h1-nr">{e(b["nr"])}</span> {e(b["titel"])}</h2><ul class="werkzeug-liste">')
        for w in liste:
            teile.append(f'<li><span class="werkzeug-art art-{slug_klein(w["art"])}">{e(w["art"])}</span>'
                         f'<div><a href="{w["link"]}">{e(w["titel"])}</a>'
                         f'<p>{e(w["text"])}</p><p class="werkzeug-thema">{e(w["thema"])}</p></div></li>')
        teile.append("</ul>")
    inhalt = teile[:3] + ['<div class="seiteninhalt">'] + teile[3:] + ["</div>"]
    return geruest(kurs, bereiche, "", "Werkzeuge", "\n".join(inhalt), aktiv_bereich="werkzeuge", toc=True)


def projekteseite(kurs, bereiche):
    """Lernprojekte: eigene Spiele und Projekte zum Kurs (kurs.json: "lernprojekte"), auf eigenen Seiten."""
    karten = []
    for p in kurs.get("lernprojekte") or []:
        karten.append(f"""<a class="karte projekt-karte" href="{e(p["url"])}" target="_blank" rel="noopener">
  <span class="karte-nr">{e(p.get("bereich", ""))}</span>
  <span class="karte-titel">{e(p["titel"])} ↗</span>
  <span class="karte-text">{e(p["text"])}</span>
  <span class="karte-fuss">{e(p.get("fuss", "läuft im Browser"))}</span>
</a>""")
    inhalt = f"""<p class="pfad"><a href="index.html">Überblick</a> › Lernprojekte</p>
<h1>Lernprojekte</h1>
<p class="unterzeile">Spiele, die für diesen Kurs entstanden sind. Sie üben genau die Inhalte des Kurses, nur anders: mit Fragen im Spiel oder mit Programmieren als Spielmechanik.</p>
<div class="karten">
{"".join(karten)}
</div>
<p class="werkzeug-hinweis">Die Lernprojekte liegen auf eigenen Seiten und öffnen sich in einem neuen Tab.</p>"""
    return geruest(kurs, bereiche, "", "Lernprojekte", inhalt, aktiv_bereich="projekte")


def slug_klein(s):
    return re.sub(r"[^a-z]+", "", s.lower().replace("ü", "ue"))


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

<h2>Mehr zum Ausprobieren</h2>
<div class="karten">
<a class="karte" href="werkzeuge.html"><span class="karte-nr">alle Themen</span><span class="karte-titel">Werkzeuge</span>
<span class="karte-text">Simulationen, Labore und interaktive Übungen aus allen Lernbereichen an einem Ort.</span></a>
<a class="karte projekt-karte" href="projekte.html"><span class="karte-nr">Spiele</span><span class="karte-titel">Lernprojekte</span>
<span class="karte-text">{e(" und ".join(p["titel"] for p in kurs.get("lernprojekte") or []))}: Spiele, die genau die Inhalte des Kurses üben.</span></a>
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
            schl = " ".join(k for _, eintraege in themen_ziele(b, t) for k, _ in eintraege)
            stand = f' data-ziele="{schl}"' if schl else ""
            teile.append(f'<li{stand}><a href="{t["slug"]}/index.html"><span class="t-nr">{e(t["nr"])}</span> {e(t["titel"])}</a>{marken}</li>')
        teile.append("</ul>")
    teile.append(lehrplan_uebersicht(b))
    return geruest(kurs, bereiche, root, f'{b["nr"]} {b["titel"]}', "\n".join(teile), aktiv_bereich=b)


# ---------------------------------------------------------------------------
# Lehrplan (linke Spalte) als Checkliste „Das kann ich jetzt“, Zuordnung in inhalt/lehrplan.json
LEHRPLAN = []            # Punkte: lb, lb_titel, ziel, text, themen, schluessel
LEHRPLAN_JE_THEMA = {}   # "bereich/thema" -> Punkte
THEMEN = {}              # "bereich/thema" -> (bereich, thema)


def lehrplan_laden(bereiche):
    LEHRPLAN.clear(); LEHRPLAN_JE_THEMA.clear(); THEMEN.clear()
    for b in bereiche:
        for k in b["kapitel"]:
            for t in k["themen_meta"]:
                THEMEN[f'{b["slug"]}/{t["slug"]}'] = (b, t)
    p = os.path.join(INHALT, "lehrplan.json")
    if not os.path.isfile(p):
        return
    daten = lies_json(p)
    anzeigen = daten.get("anzeigen")  # nur diese Lehrplan-Lernbereiche zeigen (Probelauf)
    for lb in daten["lernbereiche"]:
        if anzeigen is not None and lb["lb"] not in anzeigen:
            continue
        for z in lb["ziele"]:
            for i in z["inhalte"]:
                roh = f'{lb["lb"]}|{z["ziel"]}|{i["text"] or ""}'
                punkt = {"lb": lb["lb"], "lb_titel": lb["titel"], "ziel": z["ziel"], "text": i["text"],
                         "themen": [t for t in i["themen"] if t in THEMEN],
                         "schluessel": "lp" + hashlib.md5(roh.encode("utf-8")).hexdigest()[:10]}
                LEHRPLAN.append(punkt)
                for t in punkt["themen"]:
                    LEHRPLAN_JE_THEMA.setdefault(t, []).append(punkt)


def lehrplan_liste(punkte, links_von=None):
    """Punkte nach Lehrplan-Lernziel gruppiert; links_von = Bereich, dessen Themen verlinkt werden."""
    gruppen = []
    for p in punkte:
        if gruppen and gruppen[-1][0] == (p["lb"], p["ziel"]):
            gruppen[-1][1].append(p)
        else:
            gruppen.append(((p["lb"], p["ziel"]), [p]))
    teile = []
    for (lb, ziel), ps in gruppen:
        ohne_inhalt = len(ps) == 1 and not ps[0]["text"]
        if not ohne_inhalt:
            teile.append(f'<p class="ziel-titel"><span>LB {e(lb)}</span> {e(ziel)}</p>')
        punkte_html = []
        for p in ps:
            text = e(ziel) if ohne_inhalt else e(p["text"])
            if ohne_inhalt:
                text = f'<span class="ziel-lb">LB {e(lb)}</span> {text}'
            links = ""
            if links_von is not None:
                eigene = [THEMEN[t][1] for t in p["themen"] if THEMEN[t][0] is links_von]
                links = "".join(f' <a class="ziel-thema" href="{t["slug"]}/index.html">{e(t["nr"])}</a>' for t in eigene)
            punkte_html.append(f'<li><label><input type="checkbox" data-ziel="{p["schluessel"]}"><span>{text}</span></label>{links}</li>')
        teile.append(f'<ul class="ziele-liste">{"".join(punkte_html)}</ul>')
    return "".join(teile)


def themen_ziele(b, t):
    """Checkliste eines Themas: je Lehrplanpunkt die konkreten Punkte aus thema.json ("kann"),
    sonst der Lehrplanpunkt selbst. Liefert [(lehrplanpunkt, [(schluessel, text), ...]), ...]."""
    kann = t.get("kann") or {}
    liste = []
    for p in LEHRPLAN_JE_THEMA.get(f'{b["slug"]}/{t["slug"]}', []):
        konkret = kann.get(p["text"] or p["ziel"])
        if konkret:
            eintraege = [("k" + hashlib.md5(f'{b["slug"]}/{t["slug"]}|{k}'.encode("utf-8")).hexdigest()[:10], e(k)) for k in konkret]
        else:
            eintraege = [(p["schluessel"], e(p["text"] or p["ziel"]))]
        liste.append((p, eintraege))
    return liste


def ziele_html(b, t):
    liste = themen_ziele(b, t)
    if not liste:
        return ""
    teile = []
    for p, eintraege in liste:
        if p["text"]:
            kopf = f'{e(p["text"])} <em>({e(p["ziel"])})</em>'
        else:
            kopf = e(p["ziel"])
        teile.append(f'<p class="ziel-titel"><span>Lehrplan LB {e(p["lb"])}</span> {kopf}</p>')
        punkte = "".join(f'<li><label><input type="checkbox" data-ziel="{k}"><span>{text}</span></label></li>' for k, text in eintraege)
        teile.append(f'<ul class="ziele-liste">{punkte}</ul>')
    return f"""<section class="ziele" aria-labelledby="das-kann-ich">
<h2 id="das-kann-ich">Das kann ich jetzt</h2>
<p class="ziele-hinweis">Grau steht, was der Lehrplan verlangt, darunter, was das für dieses Thema konkret heißt. Hake einen Punkt ab, wenn er in deinem Hefter zusammengefasst ist und du ihn <strong>ohne Hilfe</strong> kannst. Wie du ihn zusammenfasst, entscheidest du selbst. Die Haken speichert nur dein Browser.</p>
{"".join(teile)}
<p class="ziele-stand" aria-live="polite"></p>
</section>"""


def lehrplan_uebersicht(b):
    punkte = [p for p in LEHRPLAN if any(THEMEN[t][0] is b for t in p["themen"])]
    if not punkte:
        return ""
    return f"""<section class="ziele" aria-labelledby="lehrplan">
<h2 id="lehrplan">Das verlangt der Lehrplan</h2>
<p class="ziele-hinweis">Alle verbindlichen Lernziele, zu denen es in diesem Lernbereich Themen gibt. Die Nummern führen zu den Themen. Haken, die du bei einem Thema setzt, erscheinen auch hier.</p>
{lehrplan_liste(punkte, links_von=b)}
<p class="ziele-stand" aria-live="polite"></p>
</section>"""


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


SVG_VOLLBILD = SVG.format('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>')
SVG_NEUER_TAB = SVG.format('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>')
SVG_ZURUECK = SVG.format('<path d="M15 18l-6-6 6-6"/>')


def zusatz_leiste(seite):
    """Knöpfe über interaktiven Zusatzseiten: Vollbild, eigener Tab ohne Kursrahmen."""
    return f"""<div class="zusatz-leiste">
<span class="zusatz-leiste-text">Interaktiv: mehr Platz?</span>
<button type="button" class="zusatz-knopf" id="vollbild-knopf">{SVG_VOLLBILD}<span>Vollbild</span></button>
<a class="zusatz-knopf nur-im-kurs" href="{seite["datei"]}?vollseite" target="_blank" rel="noopener">{SVG_NEUER_TAB}<span>In neuem Tab öffnen</span></a>
<a class="zusatz-knopf nur-vollseite" href="{seite["datei"]}">{SVG_ZURUECK}<span>Zur Kursseite</span></a>
</div>"""


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
<div class="seiteninhalt{" immer-hell" if seite.get("zusatz") else ""}" id="seiteninhalt">
{zusatz_leiste(seite) if seite.get("zusatz") else ""}
{roh}
</div>
{ziele_html(b, t) if seite["datei"] == "index.html" else ""}
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
    lehrplan_laden(bereiche)
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
    schreibe(os.path.join(SITE, "werkzeuge.html"), werkzeugseite(kurs, bereiche))
    schreibe(os.path.join(SITE, "projekte.html"), projekteseite(kurs, bereiche))
    anzahl = 5
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

# Leistungskurs Informatik – Kurswebseite

Statische Webseite für den Leistungskurs Informatik, veröffentlicht mit GitHub Pages.

- Branch `main`: Quellen (`inhalt/`, `vorlage/`, `bauen.py`)
- Branch `gh-pages`: fertig gebaute Seite, wird von `python bauen.py --veroeffentlichen` jedes Mal neu geschrieben

## Aufbau

```
inhalt/
  kurs.json                         Titel, Reihenfolge der Lernbereiche, Bildnachweise
  lb6-sprachen-automaten/
    bereich.json                    Nummer, Titel, Kurztext, Kapitel mit ihren Themen
    6-2-formale-sprache/
      thema.json                    Nummer, Titel, Unterseiten (Reiter)
      index.html                    Einführung: Theorie, Beispiele, „Das Wichtigste“, Grundaufgaben
      uebungen.html                 Übungen: weitere Aufgaben, Notebooks, Übungen für zu Hause
      vertiefung.html               Vertiefung: anspruchsvolle Aufgaben, Lösungswege
    img/  vid/  material/  notebooks/   Dateien, in den Seiten verlinkt als ../img/… usw.
vorlage/                            Stylesheets, Skripte, Icon der Seite
bauen.py                            erzeugt _site/ aus inhalt/
```

Die Seiten in `inhalt/` enthalten nur den Seiteninhalt (ohne `<html>`, `<head>`).
Kopf, Seitenleiste, Reiter und Blättern erzeugt `bauen.py`.
Die Kästen (`merke`, `aufgabe`, `beispiel klappbar`, `hinweis`, `praxisbezug` …) sind dieselben wie in OPAL.

## Ausführbarer Python-Code

Ein Codeblock `<pre class="ausfuehrbar"><code class="language-python">…</code></pre>` bekommt die Knöpfe
„Ausführen“ und „Ändern“. Ausgeführt wird mit [Natter](https://github.com/wi-wissen/Natter) im Browser
(wird erst beim ersten Klick geladen). Natter kann keine eigenen Module aus Nachbardateien, kein `csv`,
kein `typing`, keine Typangaben an Attributen (`self.x: int = …`) und kein `pow(a, b, m)` –
solche Blöcke nicht markieren. Alle anderen Codeblöcke bekommen nur „Kopieren“.

## Neues Thema anlegen

1. Ordner `inhalt/<lernbereich>/<nr-name>/` mit `thema.json`, `index.html` und bei Bedarf `uebungen.html`, `vertiefung.html` anlegen
   (am einfachsten ein vorhandenes Thema kopieren).
2. Den Ordnernamen in `bereich.json` beim passenden Kapitel eintragen.
3. Weitere Reiter (z. B. eine interaktive Zusatzseite) in `thema.json` unter `seiten` ergänzen,
   mit `"zusatz": true` bekommt der Reiter die Marke „interaktiv“.

## Lokal ansehen und veröffentlichen

```
python bauen.py --zeigen
```

Dann http://localhost:8000 öffnen. Wenn alles passt: Änderungen committen und pushen, dann

```
python bauen.py --veroeffentlichen
```

## Was nicht hierher gehört

Musterlösungen, Leistungskontrollen, Klausuren, Abiturmaterial, Schülerarbeiten und Material mit ungeklärten Rechten.

/* sortierlabor.js – interaktive Sortier-Visualisierungen für den Algorithmen-Kurs (2.2.x).

   Platzhalter in der Kursseite:
     <div class="sortierlabor" data-verfahren="bubble" data-liste="5, 2, 9, 3, 4, 6"></div>

   data-verfahren   bubble | insertion | selection | mergeteil | merge | quick | quickinplace | rennen | hochrechner
   data-liste       Startliste (Zahlen, durch Komma oder Leerzeichen getrennt)
   data-links, data-rechts   nur mergeteil: die beiden sortierten Listen
   data-auswahl     mehrere Verfahren zum Umschalten, z. B. "insertion,selection"
   data-fein        "ja": jede Codezeile ist ein eigener Schritt (sonst nur die wichtigen)
   data-vorhersage  "ja": Vorhersage-Modus ist beim Laden eingeschaltet
   data-code        "nein": ohne Code-Kasten (nur die Idee)
   data-pivot       quick: "letztes" (Standard) oder "mitte"
   data-n, data-zeit, data-klasse   hochrechner: Startwerte der Messung, Klasse n | nlogn | n2 | logn

   Die Python-Codes unten stimmen Zeile für Zeile mit den Kursseiten überein.
   Achtung OPAL: in Zeichenketten keine schließenden body- oder html-Tags (OPAL schneidet dort ab). */
(function () {
  "use strict";

  /* ---------- Python-Code der Kursseiten ---------- */
  var CODE = {
    bubble: [
      "def bubblesort(liste):",
      "    n = len(liste)",
      "    for durchlauf in range(n - 1):",
      "        getauscht = False",
      "        # die letzten 'durchlauf' Elemente stehen schon richtig",
      "        for j in range(n - 1 - durchlauf):",
      "            if liste[j] > liste[j + 1]:",
      "                temp = liste[j]",
      "                liste[j] = liste[j + 1]",
      "                liste[j + 1] = temp",
      "                getauscht = True",
      "        if not getauscht:      # kein Tausch: Liste ist sortiert",
      "            break",
      "    return liste"
    ],
    insertion: [
      "def insertion_sort(liste):",
      "    for i in range(1, len(liste)):",
      "        j = i",
      "        while j > 0:",
      "            if liste[j - 1] > liste[j]:",
      "                temp = liste[j - 1]",
      "                liste[j - 1] = liste[j]",
      "                liste[j] = temp",
      "                j = j - 1",
      "            else:",
      "                break                   # richtige Stelle gefunden",
      "    return liste"
    ],
    selection: [
      "def selection_sort(liste):",
      "    n = len(liste)",
      "    for i in range(n - 1):",
      "        min_pos = i",
      "        for j in range(i + 1, n):",
      "            if liste[j] < liste[min_pos]:",
      "                min_pos = j",
      "        if min_pos != i:",
      "            temp = liste[i]",
      "            liste[i] = liste[min_pos]",
      "            liste[min_pos] = temp",
      "    return liste"
    ],
    merge: [
      "def merge(links, rechts):",
      "    ergebnis = []",
      "    i = j = 0",
      "    while i < len(links) and j < len(rechts):",
      "        if links[i] <= rechts[j]:       # <= hält Mergesort stabil",
      "            ergebnis.append(links[i])",
      "            i = i + 1",
      "        else:",
      "            ergebnis.append(rechts[j])",
      "            j = j + 1",
      "    ergebnis.extend(links[i:])          # Rest anhängen",
      "    ergebnis.extend(rechts[j:])",
      "    return ergebnis",
      "",
      "def mergesort(liste):",
      "    if len(liste) <= 1:                 # Basisfall",
      "        return liste",
      "    mitte = len(liste) // 2",
      "    links = mergesort(liste[:mitte])    # Teilen und Herrschen",
      "    rechts = mergesort(liste[mitte:])",
      "    return merge(links, rechts)         # Kombinieren"
    ],
    quick: [
      "def quicksort(liste):",
      "    if len(liste) <= 1:",
      "        return liste",
      "    pivot = liste[len(liste) - 1]       # letzte Zahl als Pivot",
      "    kleiner = []",
      "    gleich = []",
      "    groesser = []",
      "    for x in liste:",
      "        if x < pivot:",
      "            kleiner.append(x)",
      "        elif x == pivot:",
      "            gleich.append(x)",
      "        else:",
      "            groesser.append(x)",
      "    return quicksort(kleiner) + gleich + quicksort(groesser)"
    ],
    quickinplace: [
      "def tausche(liste, a, b):",
      "    temp = liste[a]",
      "    liste[a] = liste[b]",
      "    liste[b] = temp",
      "",
      "def partitioniere(liste, links, rechts):",
      "    pivot = liste[rechts]",
      "    grenze = links",
      "    for j in range(links, rechts):",
      "        if liste[j] < pivot:",
      "            tausche(liste, grenze, j)",
      "            grenze = grenze + 1",
      "    tausche(liste, grenze, rechts)",
      "    return grenze",
      "",
      "def quicksort(liste, links, rechts):",
      "    if links < rechts:",
      "        p = partitioniere(liste, links, rechts)",
      "        quicksort(liste, links, p - 1)",
      "        quicksort(liste, p + 1, rechts)"
    ]
  };
  CODE.mergeteil = CODE.merge.slice(0, 13);
  var PIVOT_MITTE = "    pivot = liste[len(liste) // 2]      # mittlere Zahl als Pivot";

  var NAMEN = {
    bubble: "Bubblesort", insertion: "Insertionsort", selection: "Selectionsort",
    mergeteil: "merge (zwei sortierte Listen)", merge: "Mergesort",
    quick: "Quicksort (mit Teillisten)", quickinplace: "Quicksort (in place)"
  };

  /* ---------- kleine Helfer ---------- */
  function fmt(liste) { return "[" + liste.join(", ") + "]"; }
  function el(tag, klasse, text) {
    var e = document.createElement(tag);
    if (klasse) e.className = klasse;
    if (text !== undefined) e.textContent = text;
    return e;
  }
  function liesListe(text) {
    if (!text) return null;
    var teile = String(text).split(/[\s,;]+/), liste = [];
    for (var k = 0; k < teile.length; k++) {
      if (teile[k] === "") continue;
      var z = Number(teile[k]);
      if (!isFinite(z) || Math.round(z) !== z) return null;
      liste.push(z);
    }
    return liste;
  }
  function zufallsliste(n, maxWert) {
    var liste = [];
    while (liste.length < n) {
      var z = 1 + Math.floor(Math.random() * maxWert);
      if (liste.indexOf(z) < 0) liste.push(z);
    }
    return liste;
  }
  function sortiertKopie(liste) { return liste.slice().sort(function (a, b) { return a - b; }); }

  /* ---------- Aufnahme: zeichnet alle Zustände eines Laufs vorab auf ---------- */
  function Aufnahme(werte) {
    this.el = [];
    for (var k = 0; k < werte.length; k++) this.el.push({ w: werte[k], id: k });
    this.zustaende = [];
    this.v = 0;            // Vergleiche
    this.t = 0;            // Vertauschungen
    this.fertig = {};      // Positionen, die endgültig stehen
    this.vars = [];        // [[name, wert], ...]
  }
  Aufnahme.prototype.setze = function (name, wert) {
    for (var k = 0; k < this.vars.length; k++) {
      if (this.vars[k][0] === name) { this.vars[k][1] = wert; return; }
    }
    this.vars.push([name, wert]);
  };
  Aufnahme.prototype.loesche = function (name) {
    for (var k = 0; k < this.vars.length; k++) {
      if (this.vars[k][0] === name) { this.vars.splice(k, 1); return; }
    }
  };
  Aufnahme.prototype.tausch = function (a, b) {
    var x = this.el[a]; this.el[a] = this.el[b]; this.el[b] = x;
    if (a !== b) this.t++;
  };
  Aufnahme.prototype.werte = function () {
    var w = [];
    for (var k = 0; k < this.el.length; k++) w.push(this.el[k].w);
    return w;
  };
  Aufnahme.prototype.foto = function (zeile, text, opt) {
    var z = opt || {};
    z.zeile = zeile;
    z.text = text;
    z.ordnung = [];
    for (var k = 0; k < this.el.length; k++) z.ordnung.push(this.el[k].id);
    z.v = this.v;
    z.t = this.t;
    z.fertig = {};
    for (var f in this.fertig) z.fertig[f] = true;
    if (!z.vars) {
      z.vars = [];
      for (var m = 0; m < this.vars.length; m++) z.vars.push([this.vars[m][0], this.vars[m][1]]);
    }
    this.zustaende.push(z);
  };
  Aufnahme.prototype.allesFertig = function () {
    for (var k = 0; k < this.el.length; k++) this.fertig[k] = true;
  };

  function jaNein(frage, ja, erklaerung) {
    return { text: frage, optionen: ["Ja", "Nein"], richtig: ja ? 0 : 1, erkl: erklaerung };
  }

  /* ---------- Bubblesort ---------- */
  function spurBubble(werte) {
    var A = new Aufnahme(werte), a = A.el, n = a.length;
    A.setze("liste", fmt(A.werte()));
    A.foto(1, "Bubblesort bekommt die Liste " + fmt(A.werte()) + ". Verglichen werden immer zwei Nachbarn.");
    A.setze("n", n);
    A.foto(2, "n = " + n + ": So viele Zahlen hat die Liste.", { fein: true });
    for (var d = 0; d < n - 1; d++) {
      A.setze("durchlauf", d); A.loesche("j"); A.loesche("getauscht");
      A.foto(3, "Durchlauf " + d + " beginnt." + (d > 0 ? " Die letzten " + d + " Zahlen (grün) stehen schon an ihrem Platz und werden nicht mehr angefasst." : " Die größte Zahl wird bis ganz nach rechts wandern."));
      var getauscht = false;
      A.setze("getauscht", "False");
      A.foto(4, "getauscht = False: Noch wurde in diesem Durchlauf nichts getauscht.", { fein: true });
      for (var j = 0; j < n - 1 - d; j++) {
        A.setze("j", j);
        var zg = [{ name: "j", pos: j }, { name: "j+1", pos: j + 1 }];
        A.foto(6, "j = " + j + ": Jetzt sind die Plätze " + j + " und " + (j + 1) + " dran.", { fein: true, zeiger: zg });
        var gross = a[j].w > a[j + 1].w;
        A.v++;
        A.foto(7, "Vergleich: " + a[j].w + " > " + a[j + 1].w + "? " + (gross ? "Ja – die beiden stehen falsch herum." : "Nein – die beiden stehen richtig."), {
          hl: { vergleich: [j, j + 1] }, zeiger: zg,
          frage: jaNein("Vergleich von " + a[j].w + " und " + a[j + 1].w + ": Wird getauscht?", gross,
            gross ? a[j].w + " ist größer als " + a[j + 1].w + ", die größere Zahl muss nach rechts." : a[j].w + " ist nicht größer als " + a[j + 1].w + ", also bleibt alles, wie es ist.")
        });
        if (gross) {
          A.tausch(j, j + 1);
          getauscht = true;
          A.foto(8, "Getauscht: " + a[j + 1].w + " wandert eine Stelle nach rechts.", { hl: { tausch: [j, j + 1] }, zeiger: zg });
          A.setze("getauscht", "True");
          A.foto(11, "getauscht = True: Wir merken uns, dass in diesem Durchlauf etwas passiert ist.", { fein: true, zeiger: zg });
        }
      }
      A.fertig[n - 1 - d] = true;
      A.loesche("j");
      if (!getauscht) {
        A.allesFertig();
        A.foto(12, "Durchlauf " + d + " ist vorbei, und es wurde nichts getauscht. Dann muss die Liste schon sortiert sein.", {
          frage: jaNein("Durchlauf " + d + " ist vorbei. Muss Bubblesort noch einen Durchlauf machen?", false, "In diesem Durchlauf gab es keinen Tausch. Alle Nachbarn stehen richtig, also ist die Liste sortiert.")
        });
        A.foto(13, "break: Bubblesort hört vorzeitig auf.");
        break;
      }
      A.foto(12, "Durchlauf " + d + " ist vorbei. " + a[n - 1 - d].w + " steht jetzt endgültig auf Platz " + (n - 1 - d) + ". Weil getauscht wurde, geht es weiter.", { fein: d < n - 2 });
    }
    A.allesFertig();
    A.foto(14, "Fertig! Die Liste ist sortiert: " + fmt(A.werte()) + ". Dafür waren " + A.v + " Vergleiche und " + A.t + " Vertauschungen nötig.");
    return A.zustaende;
  }

  /* ---------- Insertionsort ---------- */
  function spurInsertion(werte) {
    var A = new Aufnahme(werte), a = A.el, n = a.length;
    A.setze("liste", fmt(A.werte()));
    A.foto(1, "Insertionsort bekommt die Liste " + fmt(A.werte()) + ". Die erste Zahl allein ist schon ein sortierter Teil.", { hl: { teil: [0, 1] } });
    for (var i = 1; i < n; i++) {
      A.setze("i", i); A.loesche("j");
      A.foto(2, "i = " + i + ": Die Zahl " + a[i].w + " wird jetzt in den sortierten Teil (hellgrün) eingefügt.", { hl: { teil: [0, i], aktiv: [i] }, zeiger: [{ name: "i", pos: i }] });
      var j = i;
      A.setze("j", j);
      A.foto(3, "j = " + j + ": j zeigt auf die Zahl, die gerade wandert.", { fein: true, hl: { teil: [0, i] }, zeiger: [{ name: "j", pos: j }] });
      while (j > 0) {
        A.foto(4, "j > 0? Ja, es gibt noch einen linken Nachbarn.", { fein: true, hl: { teil: [0, i + 1] }, zeiger: [{ name: "j", pos: j }] });
        var gross = a[j - 1].w > a[j].w;
        A.v++;
        A.foto(5, "Vergleich mit dem linken Nachbarn: " + a[j - 1].w + " > " + a[j].w + "? " + (gross ? "Ja – " + a[j].w + " muss weiter nach links." : "Nein – " + a[j].w + " ist an der richtigen Stelle."), {
          hl: { teil: [0, i + 1], vergleich: [j - 1, j] }, zeiger: [{ name: "j", pos: j }],
          frage: jaNein("Ist der linke Nachbar " + a[j - 1].w + " größer als " + a[j].w + "? Wandert " + a[j].w + " weiter nach links?", gross,
            gross ? a[j - 1].w + " > " + a[j].w + ", also tauschen die beiden." : a[j - 1].w + " ist nicht größer. Links davon ist alles noch kleiner, also kann " + a[j].w + " hier bleiben.")
        });
        if (gross) {
          A.tausch(j - 1, j);
          A.foto(6, "Getauscht: " + a[j - 1].w + " ist eine Stelle nach links gewandert.", { hl: { teil: [0, i + 1], tausch: [j - 1, j] }, zeiger: [{ name: "j", pos: j }] });
          j--;
          A.setze("j", j);
          A.foto(9, "j = j - 1: j zeigt wieder auf die wandernde Zahl.", { fein: true, hl: { teil: [0, i + 1] }, zeiger: [{ name: "j", pos: j }] });
        } else {
          A.foto(11, "break: Die richtige Stelle ist gefunden.", { hl: { teil: [0, i + 1] }, zeiger: [{ name: "j", pos: j }] });
          break;
        }
      }
      if (j === 0) A.foto(4, "j > 0? Nein: Die Zahl steht ganz vorn, die Schleife endet.", { hl: { teil: [0, i + 1] }, zeiger: [{ name: "j", pos: 0 }] });
    }
    A.allesFertig();
    A.loesche("i"); A.loesche("j");
    A.foto(12, "Fertig! Sortiert: " + fmt(A.werte()) + " nach " + A.v + " Vergleichen und " + A.t + " Vertauschungen.");
    return A.zustaende;
  }

  /* ---------- Selectionsort ---------- */
  function spurSelection(werte) {
    var A = new Aufnahme(werte), a = A.el, n = a.length;
    A.setze("liste", fmt(A.werte()));
    A.foto(1, "Selectionsort bekommt die Liste " + fmt(A.werte()) + ". In jeder Runde wird das Minimum des unsortierten Teils gesucht.");
    A.setze("n", n);
    A.foto(2, "n = " + n, { fein: true });
    for (var i = 0; i < n - 1; i++) {
      A.setze("i", i); A.loesche("j"); A.loesche("min_pos");
      A.foto(3, "Runde i = " + i + ": Gesucht ist die kleinste Zahl ab Platz " + i + ".", { hl: { bereich: [i, n - 1] }, zeiger: [{ name: "i", pos: i }] });
      var minPos = i;
      A.setze("min_pos", minPos);
      A.foto(4, "min_pos = " + i + ": Zuerst nehmen wir an, " + a[i].w + " ist das Minimum.", { hl: { bereich: [i, n - 1], minimum: [minPos] }, zeiger: [{ name: "i", pos: i }, { name: "min", pos: minPos }] });
      for (var j = i + 1; j < n; j++) {
        A.setze("j", j);
        var zg = [{ name: "i", pos: i }, { name: "min", pos: minPos }, { name: "j", pos: j }];
        A.foto(5, "j = " + j, { fein: true, hl: { bereich: [i, n - 1], minimum: [minPos] }, zeiger: zg });
        var kleiner = a[j].w < a[minPos].w;
        A.v++;
        A.foto(6, "Vergleich: " + a[j].w + " < " + a[minPos].w + "? " + (kleiner ? "Ja – neues Minimum." : "Nein – das Minimum bleibt " + a[minPos].w + "."), {
          hl: { bereich: [i, n - 1], minimum: [minPos], vergleich: [j, minPos] }, zeiger: zg,
          frage: jaNein("Ist " + a[j].w + " kleiner als das bisherige Minimum " + a[minPos].w + "?", kleiner,
            kleiner ? "Ja, " + a[j].w + " ist das neue Minimum. Gemerkt wird nur die Position." : "Nein, " + a[minPos].w + " bleibt das Minimum.")
        });
        if (kleiner) {
          minPos = j;
          A.setze("min_pos", minPos);
          A.foto(7, "min_pos = " + j + ": Wir merken uns nur die Stelle, getauscht wird noch nicht.", { hl: { bereich: [i, n - 1], minimum: [minPos] }, zeiger: [{ name: "i", pos: i }, { name: "min", pos: minPos }, { name: "j", pos: j }] });
        }
      }
      A.loesche("j");
      var zg2 = [{ name: "i", pos: i }, { name: "min", pos: minPos }];
      if (minPos !== i) {
        A.foto(8, "Die Suche ist fertig: Das Minimum ist " + a[minPos].w + " auf Platz " + minPos + ".", {
          hl: { bereich: [i, n - 1], minimum: [minPos] }, zeiger: zg2,
          frage: jaNein("Das Minimum " + a[minPos].w + " steht auf Platz " + minPos + ". Wird jetzt getauscht?", true, "Ja: min_pos ist nicht i, also kommt das Minimum nach vorn auf Platz " + i + ".")
        });
        A.tausch(i, minPos);
        A.fertig[i] = true;
        A.foto(9, "Tausch: " + a[i].w + " springt nach vorn auf Platz " + i + " und steht jetzt endgültig.", { hl: { tausch: [i, minPos] }, zeiger: zg2 });
      } else {
        A.fertig[i] = true;
        A.foto(8, "Das Minimum " + a[i].w + " steht schon auf Platz " + i + ". min_pos != i ist falsch, also kein Tausch.", {
          zeiger: zg2,
          frage: jaNein("Das Minimum " + a[i].w + " steht schon auf Platz " + i + ". Wird jetzt getauscht?", false, "Nein: min_pos ist gleich i, das Minimum steht schon vorn.")
        });
      }
    }
    A.allesFertig();
    A.loesche("i"); A.loesche("min_pos");
    A.foto(12, "Fertig! Sortiert: " + fmt(A.werte()) + " nach " + A.v + " Vergleichen und " + A.t + " Vertauschungen.");
    return A.zustaende;
  }

  /* ---------- merge allein (zwei sortierte Listen) ---------- */
  function mergeSchritte(A, L, R, foto, zeilenVersatz) {
    // zeichnet merge(L, R) auf; foto(zeile, text, opt) kommt vom Aufrufer
    var z = zeilenVersatz || 0;
    var erg = [], i = 0, j = 0;
    function panel(extra) {
      var p = { typ: "merge", links: L.slice(), rechts: R.slice(), i: i, j: j, ergebnis: erg.slice() };
      if (extra) for (var k in extra) p[k] = extra[k];
      return p;
    }
    function vars() {
      return [["links", fmt(L)], ["rechts", fmt(R)], ["i", i], ["j", j], ["ergebnis", fmt(erg)]];
    }
    foto(z + 1, "merge bekommt zwei sortierte Listen: " + fmt(L) + " und " + fmt(R) + ".", { panel: panel(), vars: vars() });
    foto(z + 3, "i und j zeigen auf die vorderen, noch nicht übernommenen Zahlen.", { panel: panel(), vars: vars(), fein: true });
    while (i < L.length && j < R.length) {
      var linksZuerst = L[i] <= R[j];
      A.v++;
      foto(z + 5, "Vergleich der beiden vorderen Zahlen: " + L[i] + " <= " + R[j] + "? " + (linksZuerst ? "Ja – " + L[i] + " kommt ins Ergebnis." : "Nein – " + R[j] + " kommt ins Ergebnis."), {
        panel: panel({ vergleich: true }), vars: vars(),
        frage: { text: "Welche Zahl kommt als Nächstes ins Ergebnis?", optionen: [L[i] + " (links)", R[j] + " (rechts)"], richtig: linksZuerst ? 0 : 1,
          erkl: "Die kleinere der beiden vorderen Zahlen kommt ins Ergebnis" + (L[i] === R[j] ? ". Bei Gleichstand nimmt merge die linke (<=), so bleibt Mergesort stabil." : ".") }
      });
      if (linksZuerst) {
        erg.push(L[i]); i++;
        foto(z + 6, L[i - 1] + " wird angehängt, i rückt weiter.", { panel: panel({ neu: true }), vars: vars() });
      } else {
        erg.push(R[j]); j++;
        foto(z + 9, R[j - 1] + " wird angehängt, j rückt weiter.", { panel: panel({ neu: true }), vars: vars() });
      }
    }
    var restL = L.slice(i), restR = R.slice(j);
    var leer = (i >= L.length) ? "links" : "rechts";
    foto(z + 4, "Die Liste " + leer + " ist aufgebraucht – die Schleife endet. Ab jetzt sind keine Vergleiche mehr nötig.", { panel: panel(), vars: vars(), fein: true });
    for (var k = 0; k < restL.length; k++) erg.push(restL[k]);
    i = L.length;
    foto(z + 11, restL.length ? "Rest von links anhängen: " + fmt(restL) + " – ohne Vergleich, denn der Rest ist schon sortiert und größer." : "links[i:] ist leer, hier wird nichts angehängt.", { panel: panel({ neu: restL.length > 0 }), vars: vars(), fein: restL.length === 0 });
    for (var m = 0; m < restR.length; m++) erg.push(restR[m]);
    j = R.length;
    foto(z + 12, restR.length ? "Rest von rechts anhängen: " + fmt(restR) + " – ohne Vergleich." : "rechts[j:] ist leer, hier wird nichts angehängt.", { panel: panel({ neu: restR.length > 0 }), vars: vars(), fein: restR.length === 0 });
    return erg;
  }

  function spurMergeTeil(L, R) {
    var A = new Aufnahme([]);
    function foto(zeile, text, opt) { A.foto(zeile, text, opt); }
    var erg = mergeSchritte(A, L, R, foto, 0);
    A.foto(13, "Fertig: merge gibt " + fmt(erg) + " zurück. Das waren " + A.v + " Vergleiche (höchstens " + L.length + " + " + R.length + " − 1 = " + (L.length + R.length - 1) + ").", {
      panel: { typ: "merge", links: L, rechts: R, i: L.length, j: R.length, ergebnis: erg, fertig: true }, vars: [["ergebnis", fmt(erg)]]
    });
    return A.zustaende;
  }

  /* ---------- Baum-Helfer für Mergesort und Quicksort ---------- */
  function Baum() { this.knoten = []; this.stapel = []; }
  Baum.prototype.neu = function (von, werte, tiefe, status) {
    this.knoten.push({ von: von, bis: von + werte.length, tiefe: tiefe, werte: werte.slice(), status: status || "offen" });
    return this.knoten.length - 1;
  };
  Baum.prototype.kopie = function () {
    var k = [];
    for (var m = 0; m < this.knoten.length; m++) {
      var x = this.knoten[m];
      k.push({ von: x.von, bis: x.bis, tiefe: x.tiefe, werte: x.werte.slice(), status: x.status, leer: x.leer, markiert: x.markiert, pivotPos: x.pivotPos });
    }
    return k;
  };

  /* ---------- Mergesort ---------- */
  function spurMerge(werte) {
    var A = new Aufnahme([]), B = new Baum();
    var aktiv = -1;
    function foto(zeile, text, opt) {
      opt = opt || {};
      opt.baum = B.kopie();
      opt.aktiv = aktiv;
      opt.stapel = B.stapel.slice();
      A.foto(zeile, text, opt);
    }
    function ms(liste, von, tiefe) {
      var id = B.neu(von, liste, tiefe), vorher = aktiv;
      aktiv = id;
      B.stapel.push("mergesort(" + fmt(liste) + ")");
      var v = [["liste", fmt(liste)]];
      foto(15, "Aufruf mergesort(" + fmt(liste) + ").", { vars: v });
      if (liste.length <= 1) {
        B.knoten[id].status = "sortiert";
        foto(16, "Basisfall: Eine Liste mit " + (liste.length === 1 ? "einem Element" : "keinem Element") + " ist schon sortiert. Sie wird unverändert zurückgegeben.", { vars: v });
        B.stapel.pop();
        aktiv = vorher;
        return liste;
      }
      var mitte = Math.floor(liste.length / 2);
      var lTeil = liste.slice(0, mitte), rTeil = liste.slice(mitte);
      v.push(["mitte", mitte]);
      B.knoten[id].status = "geteilt";
      foto(18, "Teilen: mitte = " + liste.length + " // 2 = " + mitte + ". Links " + fmt(lTeil) + ", rechts " + fmt(rTeil) + ".", { vars: v });
      foto(19, "Zuerst wird die linke Hälfte " + fmt(lTeil) + " sortiert – mit einem neuen Aufruf von mergesort.", { vars: v, fein: true });
      var L = ms(lTeil, von, tiefe + 1);
      aktiv = id;
      v.push(["links", fmt(L)]);
      foto(20, "Zurück im Aufruf mergesort(" + fmt(liste) + "): links ist jetzt sortiert, " + fmt(L) + ". Jetzt kommt die rechte Hälfte " + fmt(rTeil) + " dran.", { vars: v });
      var R = ms(rTeil, von + mitte, tiefe + 1);
      aktiv = id;
      v.push(["rechts", fmt(R)]);
      foto(21, "Beide Hälften sind sortiert: " + fmt(L) + " und " + fmt(R) + ". Jetzt führt merge sie zusammen.", { vars: v });
      B.stapel.push("merge(" + fmt(L) + ", " + fmt(R) + ")");
      B.knoten[id].status = "merge";
      B.knoten[id].werte = [];
      B.knoten[id].leer = liste.length;
      var erg = mergeSchritte(A, L, R, function (zeile, text, opt) {
        B.knoten[id].werte = opt.panel.ergebnis.slice();
        foto(zeile, text, opt);
      }, 0);
      B.stapel.pop();
      B.knoten[id].werte = erg;
      B.knoten[id].leer = 0;
      B.knoten[id].status = "sortiert";
      foto(21, "mergesort(" + fmt(liste) + ") gibt die sortierte Liste " + fmt(erg) + " zurück.", { vars: [["liste", fmt(liste)], ["ergebnis", fmt(erg)]] });
      B.stapel.pop();
      aktiv = vorher;
      return erg;
    }
    var erg = ms(werte.slice(), 0, 0);
    foto(21, "Fertig! Mergesort hat " + fmt(erg) + " geliefert – mit " + A.v + " Vergleichen. Alle Vergleiche passieren beim Zusammenführen (merge).", { vars: [["ergebnis", fmt(erg)]] });
    return A.zustaende;
  }

  /* ---------- Quicksort mit Teillisten ---------- */
  function spurQuick(werte, pivotwahl) {
    var A = new Aufnahme([]), B = new Baum();
    var aktiv = -1;
    var pzeile = 4;
    function foto(zeile, text, opt) {
      opt = opt || {};
      opt.baum = B.kopie();
      opt.aktiv = aktiv;
      opt.stapel = B.stapel.slice();
      A.foto(zeile, text, opt);
    }
    function qs(liste, von, tiefe) {
      var vorher = aktiv, id = -1;
      if (liste.length > 0) { id = B.neu(von, liste, tiefe); aktiv = id; }
      B.stapel.push("quicksort(" + fmt(liste) + ")");
      var v = [["liste", fmt(liste)]];
      if (liste.length <= 1) {
        if (id >= 0) B.knoten[id].status = "sortiert";
        foto(2, "Aufruf quicksort(" + fmt(liste) + "): Basisfall – " + (liste.length ? "eine Zahl allein" : "eine leere Liste") + " ist sortiert.", { vars: v });
        B.stapel.pop();
        aktiv = vorher;
        return liste;
      }
      var pPos = (pivotwahl === "mitte") ? Math.floor(liste.length / 2) : liste.length - 1;
      var pivot = liste[pPos];
      B.knoten[id].pivotPos = pPos;
      v.push(["pivot", pivot]);
      foto(1, "Aufruf quicksort(" + fmt(liste) + ").", { vars: [["liste", fmt(liste)]] });
      foto(pzeile, "Pivot ist " + pivot + " (" + (pivotwahl === "mitte" ? "die mittlere Zahl" : "die letzte Zahl") + "). Jede Zahl wird jetzt mit " + pivot + " verglichen.", { vars: v });
      var kl = [], gl = [], gr = [];
      function panel(x) { return { typ: "partition", pivot: pivot, kleiner: kl.slice(), gleich: gl.slice(), groesser: gr.slice(), x: x }; }
      function pv(x) { return v.concat([["x", x === undefined ? "–" : x], ["kleiner", fmt(kl)], ["gleich", fmt(gl)], ["groesser", fmt(gr)]]); }
      foto(5, "Drei leere Listen für die Zahlen kleiner, gleich und größer als " + pivot + ".", { panel: panel(), vars: pv(), fein: true });
      for (var k = 0; k < liste.length; k++) {
        var x = liste[k];
        B.knoten[id].markiert = k;
        var ziel = x < pivot ? 0 : (x === pivot ? 1 : 2);
        A.v++;
        foto(9, "x = " + x + ": Vergleich mit dem Pivot " + pivot + ".", {
          panel: panel(x), vars: pv(x),
          frage: { text: "Wohin kommt " + x + "?", optionen: ["kleiner", "gleich", "größer"], richtig: ziel,
            erkl: x + (ziel === 0 ? " < " : (ziel === 1 ? " = " : " > ")) + pivot + ", also in die Liste " + ["kleiner", "gleich", "groesser"][ziel] + "." }
        });
        if (ziel === 0) kl.push(x); else if (ziel === 1) gl.push(x); else gr.push(x);
        foto([10, 12, 14][ziel], x + " kommt in " + ["kleiner", "gleich", "groesser"][ziel] + ".", { panel: panel(), vars: pv(x), fein: true });
      }
      B.knoten[id].markiert = undefined;
      B.knoten[id].status = "geteilt";
      var gid = B.neu(von + kl.length, gl, tiefe + 1, "pivot");
      foto(15, "Aufteilen fertig: " + fmt(kl) + " | " + fmt(gl) + " | " + fmt(gr) + ". Das Pivot steht damit schon an seinem endgültigen Platz. Jetzt werden die beiden Teile sortiert.", { panel: panel(), vars: pv() });
      var K = qs(kl, von, tiefe + 1);
      aktiv = id;
      var G = qs(gr, von + kl.length + gl.length, tiefe + 1);
      aktiv = id;
      var erg = K.concat(gl).concat(G);
      B.knoten[id].werte = erg;
      B.knoten[id].status = "sortiert";
      foto(15, "Zusammensetzen: " + fmt(K) + " + " + fmt(gl) + " + " + fmt(G) + " = " + fmt(erg) + ". Hier wird nichts mehr verglichen – die Arbeit steckte im Aufteilen.", { vars: [["liste", fmt(liste)], ["pivot", pivot], ["ergebnis", fmt(erg)]] });
      B.stapel.pop();
      aktiv = vorher;
      return erg;
    }
    var erg = qs(werte.slice(), 0, 0);
    aktiv = 0;
    foto(15, "Fertig! Quicksort hat " + fmt(erg) + " geliefert – mit " + A.v + " Vergleichen mit dem Pivot.", { vars: [["ergebnis", fmt(erg)]] });
    return A.zustaende;
  }

  /* ---------- Quicksort in place (Partitionieren nach Lomuto) ---------- */
  function spurQuickInPlace(werte) {
    var A = new Aufnahme(werte), a = A.el, n = a.length;
    var stapel = [];
    function foto(zeile, text, opt) {
      opt = opt || {};
      opt.stapel = stapel.slice();
      A.foto(zeile, text, opt);
    }
    function qs(links, rechts) {
      stapel.push("quicksort(liste, " + links + ", " + rechts + ")");
      var v = [["links", links], ["rechts", rechts]];
      if (!(links < rechts)) {
        if (links === rechts) A.fertig[links] = true;
        foto(17, "quicksort(liste, " + links + ", " + rechts + "): links < rechts ist falsch – " + (links === rechts ? "ein Bereich mit einer Zahl ist sortiert." : "der Bereich ist leer.") + " Nichts zu tun.", { vars: v, hl: links === rechts ? { bereich: [links, rechts] } : {} });
        stapel.pop();
        return;
      }
      foto(17, "quicksort(liste, " + links + ", " + rechts + "): Bereich von Platz " + links + " bis " + rechts + " wird sortiert.", { vars: v, hl: { bereich: [links, rechts] } });
      stapel.push("partitioniere(liste, " + links + ", " + rechts + ")");
      var pivot = a[rechts].w;
      var pv = [["links", links], ["rechts", rechts], ["pivot", pivot]];
      foto(7, "Pivot ist die rechte Zahl im Bereich: " + pivot + ".", { vars: pv, hl: { bereich: [links, rechts], pivot: [rechts] } });
      var grenze = links;
      function hl(extra) {
        var h = { bereich: [links, rechts], pivot: [rechts], klein: [links, grenze], gross: [grenze, extra && extra.j !== undefined ? extra.j : grenze] };
        if (extra) for (var k in extra) if (k !== "j") h[k] = extra[k];
        return h;
      }
      foto(8, "grenze = " + links + ": Links von grenze sammeln sich gleich die Zahlen, die kleiner als " + pivot + " sind (blau).", { vars: pv.concat([["grenze", grenze]]), hl: hl(), zeiger: [{ name: "grenze", pos: grenze }], fein: true });
      for (var j = links; j < rechts; j++) {
        var zg = [{ name: "grenze", pos: grenze }, { name: "j", pos: j }];
        var vj = pv.concat([["grenze", grenze], ["j", j]]);
        var klein = a[j].w < pivot;
        A.v++;
        foto(10, "Vergleich: " + a[j].w + " < " + pivot + "? " + (klein ? "Ja – " + a[j].w + " gehört in den blauen Teil." : "Nein – " + a[j].w + " bleibt im orangen Teil."), {
          vars: vj, hl: hl({ j: j, vergleich: [j, rechts] }), zeiger: zg,
          frage: jaNein("Ist " + a[j].w + " kleiner als das Pivot " + pivot + "?", klein,
            klein ? a[j].w + " < " + pivot + ": " + a[j].w + " wird an die Stelle grenze getauscht, dann rückt grenze eins weiter." : a[j].w + " ist nicht kleiner. Es bleibt, wo es ist, und j geht weiter.")
        });
        if (klein) {
          var g = grenze;
          A.tausch(grenze, j);
          foto(11, g === j ? "tausche(liste, " + g + ", " + j + "): Die Zahl steht schon an der Grenze, sie wird mit sich selbst getauscht." : "tausche(liste, " + g + ", " + j + "): " + a[g].w + " kommt nach links in den blauen Teil.", {
            vars: vj, hl: hl({ j: j + 1, tausch: g === j ? [] : [g, j] }), zeiger: zg
          });
          grenze++;
          foto(12, "grenze = grenze + 1 = " + grenze + ".", { vars: pv.concat([["grenze", grenze], ["j", j]]), hl: hl({ j: j + 1 }), zeiger: [{ name: "grenze", pos: grenze }, { name: "j", pos: j }], fein: true });
        }
      }
      var gAlt = grenze;
      foto(13, "Alle Zahlen sind verglichen. Jetzt kommt das Pivot " + pivot + " an die Grenze (Platz " + grenze + ").", {
        vars: pv.concat([["grenze", grenze]]), hl: hl({ j: rechts }), zeiger: [{ name: "grenze", pos: grenze }]
      });
      A.tausch(grenze, rechts);
      A.fertig[grenze] = true;
      foto(13, "Das Pivot " + pivot + " steht jetzt endgültig auf Platz " + gAlt + ": links nur kleinere, rechts nur größere oder gleiche Zahlen.", {
        vars: pv.concat([["grenze", grenze]]), hl: { bereich: [links, rechts], klein: [links, gAlt], gross: [gAlt + 1, rechts + 1], tausch: gAlt === rechts ? [] : [gAlt, rechts] }, zeiger: [{ name: "grenze", pos: gAlt }]
      });
      stapel.pop();
      var p = gAlt;
      foto(18, "partitioniere gibt p = " + p + " zurück. Links davon: Platz " + links + " bis " + (p - 1) + ", rechts davon: Platz " + (p + 1) + " bis " + rechts + ".", { vars: v.concat([["p", p]]), hl: { bereich: [links, rechts] } });
      foto(19, "Erst wird der linke Teil sortiert: quicksort(liste, " + links + ", " + (p - 1) + ").", { vars: v.concat([["p", p]]), hl: { bereich: [links, p - 1] }, fein: true });
      qs(links, p - 1);
      foto(20, "Zurück in quicksort(liste, " + links + ", " + rechts + "): jetzt der rechte Teil, quicksort(liste, " + (p + 1) + ", " + rechts + ").", { vars: v.concat([["p", p]]), hl: { bereich: [p + 1, rechts] }, fein: true });
      qs(p + 1, rechts);
      stapel.pop();
    }
    foto(16, "Quicksort bekommt die ganze Liste: links = 0, rechts = " + (n - 1) + ".", { vars: [["liste", fmt(A.werte())]] });
    qs(0, n - 1);
    A.allesFertig();
    foto(20, "Fertig! Die Liste ist sortiert: " + fmt(A.werte()) + " – mit " + A.v + " Vergleichen und " + A.t + " Vertauschungen, ganz ohne zusätzliche Listen.", { vars: [["liste", fmt(A.werte())]] });
    return A.zustaende;
  }

  /* ---------- Stil ---------- */
  function stil() {
    if (document.getElementById("sortierlabor-stil")) return;
    var css = document.createElement("style");
    css.id = "sortierlabor-stil";
    css.textContent = [
      ".sl{border:1px solid #c7d2fe;border-radius:10px;padding:0.9rem 1rem;margin:1.2rem 0;background:#fbfcff;font-size:0.95rem}",
      ".sl-titel{font-weight:bold;color:#1e3a8a;margin-bottom:0.4em}",
      ".sl-zeile{display:flex;flex-wrap:wrap;gap:0.5em 0.9em;align-items:center;margin:0.45em 0}",
      ".sl button,.sl select,.sl input{font:inherit;font-size:0.92rem}",
      ".sl button{padding:0.3em 0.8em;border:1px solid #1d4ed8;border-radius:6px;background:#fff;color:#1d4ed8;cursor:pointer}",
      ".sl button.haupt{background:#1d4ed8;color:#fff}",
      ".sl button:disabled{opacity:0.4;cursor:default}",
      ".sl input[type=text]{width:16em;padding:0.25em 0.5em;border:1px solid #c9ced8;border-radius:6px;font-family:Consolas,monospace}",
      ".sl-fehler{color:#b91c1c;font-size:0.9rem}",
      ".sl-buehne{position:relative;background:#fff;border:1px solid #e2e2e2;border-radius:8px;margin:0.6em 0;overflow:hidden}",
      ".sl-el{position:absolute;bottom:90px;transition:left 0.45s ease;text-align:center}",
      ".sl-balken{margin:0 auto;width:62%;border-radius:4px 4px 0 0;background:#93c5fd;transition:background 0.2s}",
      ".sl-karte{position:absolute;left:50%;transform:translateX(-50%);top:100%;margin-top:4px;min-width:30px;padding:3px 4px;border:2px solid #334155;border-radius:6px;background:#fff;font-weight:bold;font-family:Consolas,monospace;font-size:1rem;line-height:1.2;transition:background 0.2s,border-color 0.2s}",
      ".sl-el.vergleich .sl-karte{background:#fde68a;border-color:#b45309}.sl-el.vergleich .sl-balken{background:#f59e0b}",
      ".sl-el.tausch .sl-karte{background:#fecaca;border-color:#b91c1c}.sl-el.tausch .sl-balken{background:#ef4444}",
      ".sl-el.teil .sl-balken{background:#86efac}",
      ".sl-el.fertig .sl-karte{background:#bbf7d0;border-color:#15803d}.sl-el.fertig .sl-balken{background:#22c55e}",
      ".sl-el.minimum .sl-karte{border-color:#1d4ed8;box-shadow:0 0 0 2px #93c5fd}.sl-el.minimum .sl-balken{background:#1d4ed8}",
      ".sl-el.pivot .sl-karte{background:#e9d5ff;border-color:#7e22ce}.sl-el.pivot .sl-balken{background:#a855f7}",
      ".sl-el.klein .sl-balken{background:#60a5fa}.sl-el.gross .sl-balken{background:#fdba74}",
      ".sl-el.aus{opacity:0.28}",
      ".sl-el.aktiv .sl-karte{box-shadow:0 0 0 3px #fbbf24}",
      ".sl-index{position:absolute;bottom:38px;font-size:0.72rem;color:#9ca3af;text-align:center}",
      ".sl-zeiger{position:absolute;font-size:0.78rem;font-weight:bold;color:#fff;background:#1d4ed8;border-radius:4px;padding:0 4px;transition:left 0.35s ease;white-space:nowrap}",
      ".sl-zeiger.z1{background:#7c3aed}.sl-zeiger.z2{background:#0f766e}",
      ".sl-meldung{background:#eef2ff;border-left:4px solid #1d4ed8;border-radius:6px;padding:0.55em 0.85em;min-height:2.8em}",
      ".sl-meldung.frage{background:#fff7e6;border-left-color:#b45309}",
      ".sl-meldung.richtig{background:#ecfdf5;border-left-color:#15803d}",
      ".sl-meldung.falsch{background:#fdeceb;border-left-color:#d64545}",
      ".sl-antworten{display:flex;gap:0.5em;flex-wrap:wrap;margin-top:0.45em}",
      ".sl-antworten button{background:#fff7e6;border-color:#b45309;color:#7c2d12;font-weight:bold}",
      ".sl-info{font-size:0.88rem;color:#4b5563}",
      ".sl-info b{color:#111827}",
      ".sl-unten{display:grid;grid-template-columns:3fr 2fr;gap:0.8em;margin-top:0.6em}",
      "@media (max-width:720px){.sl-unten{grid-template-columns:1fr}}",
      ".sl-code{margin:0;font-size:0.8rem;line-height:1.45;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;padding:0.4em 0;overflow-x:auto}",
      ".sl-code span.z{display:block;padding:0 0.5em;white-space:pre}",
      ".sl-code span.z.an{background:#fde68a}",
      ".sl-code span.nr{color:#9ca3af;display:inline-block;width:2.2em;user-select:none}",
      ".sl-kasten{border:1px solid #e2e8f0;border-radius:6px;background:#fff;padding:0.35em 0.6em;margin-bottom:0.6em;font-size:0.85rem}",
      ".sl-kasten h4{margin:0 0 0.3em 0;font-size:0.85rem;color:#1e3a8a}",
      ".sl-kasten table{margin:0;width:100%;border-collapse:collapse}",
      ".sl-kasten td{padding:0.1em 0.4em;font-family:Consolas,monospace;font-size:0.82rem;border:none;text-align:left;background:none}",
      ".sl-kasten td:first-child{color:#6b7280;width:1%;white-space:nowrap}",
      ".sl-kasten tr.neu td{background:#fef9c3}",
      ".sl-stapel div{font-family:Consolas,monospace;font-size:0.8rem;padding:0.15em 0.4em;border:1px solid #c7d2fe;border-radius:4px;margin:0.15em 0;background:#eef2ff}",
      ".sl-stapel div:first-of-type{background:#fde68a;border-color:#b45309}",
      ".sl-baum{position:relative;margin:0.6em 0;background:#fff;border:1px solid #e2e2e2;border-radius:8px;overflow:hidden}",
      ".sl-knoten{position:absolute;box-sizing:border-box;border:1.5px solid #94a3b8;border-radius:7px;background:#fff;display:flex;justify-content:space-around;align-items:center;padding:0 1px;transition:background 0.2s}",
      ".sl-knoten.geteilt{border-style:dashed;background:#f8fafc;color:#94a3b8}",
      ".sl-knoten.merge{border-color:#b45309;background:#fffbeb}",
      ".sl-knoten.sortiert{border-color:#15803d;background:#dcfce7}",
      ".sl-knoten.pivot{border-color:#7e22ce;background:#f3e8ff}",
      ".sl-knoten.aktiv{box-shadow:0 0 0 3px #1d4ed8}",
      ".sl-knoten span{font-family:Consolas,monospace;font-weight:bold;font-size:0.9rem;min-width:1.2em;text-align:center;border-radius:4px}",
      ".sl-knoten span.leer{color:transparent;border-bottom:2px dotted #d97706;min-width:1.4em}",
      ".sl-knoten span.mark{background:#fde68a}",
      ".sl-knoten span.piv{background:#e9d5ff;color:#581c87}",
      ".sl-ebene{position:absolute;left:4px;font-size:0.7rem;color:#9ca3af}",
      ".sl-panel{margin:0.5em 0}",
      ".sl-reihe{display:flex;align-items:center;gap:0.35em;margin:0.25em 0;min-height:2.3em;flex-wrap:wrap}",
      ".sl-reihe .lab{width:6.2em;font-size:0.85rem;color:#4b5563;text-align:right;padding-right:0.3em}",
      ".sl-mk{position:relative;min-width:2.1em;padding:0.2em 0.3em;text-align:center;border:2px solid #334155;border-radius:6px;background:#fff;font-weight:bold;font-family:Consolas,monospace}",
      ".sl-mk.weg{opacity:0.25}",
      ".sl-mk.vorn{border-color:#b45309;background:#fde68a}",
      ".sl-mk.neu{background:#bbf7d0;border-color:#15803d}",
      ".sl-mk.piv{background:#e9d5ff;border-color:#7e22ce}",
      ".sl-mk .pf{position:absolute;left:50%;transform:translateX(-50%);top:100%;font-size:0.7rem;color:#1d4ed8}",
      ".sl-leer{color:#9ca3af;font-style:italic;font-size:0.85rem}",
      ".sl-legende{display:flex;flex-wrap:wrap;gap:0.3em 1em;font-size:0.8rem;color:#4b5563;margin-top:0.3em}",
      ".sl-legende i{display:inline-block;width:0.9em;height:0.9em;border-radius:3px;vertical-align:-0.1em;margin-right:0.3em;border:1px solid #64748b}",
      ".sl-rennen-gitter{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:0.7em;margin:0.6em 0}",
      ".sl-bahn{border:1px solid #e2e2e2;border-radius:8px;background:#fff;padding:0.4em 0.5em}",
      ".sl-bahn h4{margin:0 0 0.3em 0;font-size:0.9rem;display:flex;justify-content:space-between}",
      ".sl-bahn .flaeche{position:relative;height:110px;display:flex;align-items:flex-end;gap:1px}",
      ".sl-bahn .flaeche div{flex:1;background:#93c5fd;border-radius:1px 1px 0 0}",
      ".sl-bahn .flaeche div.v{background:#f59e0b}.sl-bahn .flaeche div.s{background:#ef4444}",
      ".sl-bahn.fertig{border-color:#15803d;background:#f0fdf4}",
      ".sl-bahn.fertig .flaeche div{background:#22c55e}",
      ".sl-platz{font-weight:bold;color:#15803d}",
      ".sl table th{white-space:nowrap}",
      ".sl-diagramm{width:100%;height:auto;background:#fff;border:1px solid #e2e2e2;border-radius:6px;margin-top:0.5em}"
    ].join("\n");
    document.head.appendChild(css);
  }

  /* ---------- Labor: Steuerung und Darstellung ---------- */
  var STANDARD = {
    bubble: [5, 2, 9, 3, 4, 6], insertion: [5, 2, 9, 3, 4, 6], selection: [5, 2, 9, 3, 4, 6],
    merge: [38, 27, 43, 3, 9, 82, 10], quick: [5, 8, 2, 9, 1, 7, 3, 6], quickinplace: [5, 8, 2, 9, 1, 7, 3, 6]
  };
  var BAUM = { merge: true, quick: true };
  var GRENZE = { merge: 16, quick: 16 };

  function Labor(wurzel) {
    this.w = wurzel;
    var d = wurzel.dataset;
    this.verfahren = d.verfahren || "bubble";
    this.auswahl = d.auswahl ? d.auswahl.split(/\s*,\s*/) : null;
    if (this.auswahl && this.auswahl.indexOf(this.verfahren) < 0) this.verfahren = this.auswahl[0];
    this.fein = d.fein === "ja";
    this.vorhersage = d.vorhersage === "ja";
    this.mitCode = d.code !== "nein";
    this.pivotwahl = d.pivot === "mitte" ? "mitte" : "letztes";
    this.startListe = liesListe(d.liste) || STANDARD[this.verfahren] || [5, 2, 9, 3, 4, 6];
    this.liste = this.startListe.slice();
    this.links = liesListe(d.links) || [3, 8];
    this.rechts = liesListe(d.rechts) || [2, 5];
    this.timer = null;
    this.antworten = {};
    this.bauen();
    this.neu();
    var self = this;
    window.addEventListener("resize", function () { self.zeichnen(true); });
  }

  Labor.prototype.bauen = function () {
    var self = this, w = this.w;
    w.innerHTML = "";
    w.classList.add("sl");
    this.titel = el("div", "sl-titel");
    w.appendChild(this.titel);

    // Zeile 1: Verfahren, Liste
    var z1 = el("div", "sl-zeile");
    if (this.auswahl) {
      var lab = el("label", null, "Verfahren: ");
      this.wahl = el("select");
      for (var k = 0; k < this.auswahl.length; k++) {
        var o = el("option", null, NAMEN[this.auswahl[k]]);
        o.value = this.auswahl[k];
        this.wahl.appendChild(o);
      }
      this.wahl.value = this.verfahren;
      this.wahl.addEventListener("change", function () { self.verfahren = self.wahl.value; self.neu(); });
      lab.appendChild(this.wahl);
      z1.appendChild(lab);
    }
    if (this.verfahren === "mergeteil") {
      var l1 = el("label", null, "links: "); this.eingabeL = el("input"); this.eingabeL.type = "text"; this.eingabeL.style.width = "9em"; l1.appendChild(this.eingabeL);
      var l2 = el("label", null, "rechts: "); this.eingabeR = el("input"); this.eingabeR.type = "text"; this.eingabeR.style.width = "9em"; l2.appendChild(this.eingabeR);
      z1.appendChild(l1); z1.appendChild(l2);
    } else {
      var l3 = el("label", null, "Liste: ");
      this.eingabe = el("input"); this.eingabe.type = "text";
      l3.appendChild(this.eingabe);
      z1.appendChild(l3);
    }
    var uebernehmen = el("button", null, "Übernehmen");
    uebernehmen.type = "button";
    uebernehmen.addEventListener("click", function () { self.uebernehmen(); });
    z1.appendChild(uebernehmen);
    var eingaben = z1.querySelectorAll("input");
    for (var e = 0; e < eingaben.length; e++) {
      eingaben[e].addEventListener("keydown", function (ev) { if (ev.key === "Enter") self.uebernehmen(); });
    }
    w.appendChild(z1);

    var z2 = el("div", "sl-zeile");
    if (this.verfahren === "mergeteil") {
      this.knopf(z2, "Neue Zufallslisten", function () {
        var alle = sortiertKopie(zufallsliste(7, 40));
        var l = [], r = [];
        for (var k = 0; k < alle.length; k++) { if (Math.random() < 0.5) l.push(alle[k]); else r.push(alle[k]); }
        if (!l.length) l.push(r.shift());
        if (!r.length) r.push(l.pop());
        self.links = l; self.rechts = r; self.neu();
      });
    } else {
      this.knopf(z2, "Mischen", function () { self.liste = zufallsliste(self.liste.length || 8, Math.max(20, 3 * (self.liste.length || 8))); self.neu(); });
      this.knopf(z2, "Schon sortiert", function () { self.liste = sortiertKopie(self.liste); self.neu(); });
      this.knopf(z2, "Absteigend", function () { self.liste = sortiertKopie(self.liste).reverse(); self.neu(); });
      this.knopf(z2, "Startliste", function () { self.liste = self.startListe.slice(); self.neu(); });
      if (this.verfahren === "quick" || (this.auswahl && this.auswahl.indexOf("quick") >= 0)) {
        var lp = el("label", null, "Pivot: ");
        this.pivotSel = el("select");
        var o1 = el("option", null, "letzte Zahl"); o1.value = "letztes";
        var o2 = el("option", null, "mittlere Zahl"); o2.value = "mitte";
        this.pivotSel.appendChild(o1); this.pivotSel.appendChild(o2);
        this.pivotSel.value = this.pivotwahl;
        this.pivotSel.addEventListener("change", function () { self.pivotwahl = self.pivotSel.value; self.neu(); });
        lp.appendChild(this.pivotSel);
        z2.appendChild(lp);
      }
    }
    this.fehler = el("span", "sl-fehler");
    z2.appendChild(this.fehler);
    w.appendChild(z2);

    // Bühne
    this.buehne = el("div", "sl-buehne");
    w.appendChild(this.buehne);
    this.panelEl = el("div", "sl-panel");
    w.appendChild(this.panelEl);
    this.legende = el("div", "sl-legende");
    w.appendChild(this.legende);

    // Meldung
    this.meldung = el("div", "sl-meldung");
    this.meldung.setAttribute("aria-live", "polite");
    w.appendChild(this.meldung);

    // Steuerung
    var z3 = el("div", "sl-zeile");
    this.bAnfang = this.knopf(z3, "⏮ Anfang", function () { self.stopp(); self.geheZu(0); });
    this.bZurueck = this.knopf(z3, "◀ Zurück", function () { self.stopp(); self.schritt(-1); });
    this.bWeiter = this.knopf(z3, "Weiter ▶", function () { self.stopp(); self.schritt(1); }, "haupt");
    this.bSpielen = this.knopf(z3, "▶▶ Abspielen", function () { self.spielen(); });
    var tl = el("label", "sl-info", "Tempo ");
    this.tempo = el("input"); this.tempo.type = "range"; this.tempo.min = "1"; this.tempo.max = "10"; this.tempo.value = "5";
    this.tempo.style.width = "6em"; this.tempo.style.verticalAlign = "middle";
    tl.appendChild(this.tempo);
    z3.appendChild(tl);
    w.appendChild(z3);

    var z4 = el("div", "sl-zeile");
    this.info = el("span", "sl-info");
    z4.appendChild(this.info);
    w.appendChild(z4);

    var z5 = el("div", "sl-zeile");
    var c1 = el("label", "sl-info");
    this.cbVorhersage = el("input"); this.cbVorhersage.type = "checkbox"; this.cbVorhersage.checked = this.vorhersage;
    c1.appendChild(this.cbVorhersage); c1.appendChild(document.createTextNode(" Ich sage vorher, was passiert"));
    this.cbVorhersage.addEventListener("change", function () { self.vorhersage = self.cbVorhersage.checked; self.zeichnen(); });
    z5.appendChild(c1);
    if (this.mitCode) {
      var c2 = el("label", "sl-info");
      this.cbFein = el("input"); this.cbFein.type = "checkbox"; this.cbFein.checked = this.fein;
      c2.appendChild(this.cbFein); c2.appendChild(document.createTextNode(" Jede Codezeile einzeln"));
      this.cbFein.addEventListener("change", function () { self.fein = self.cbFein.checked; self.sichtbarBerechnen(); self.zeichnen(); });
      z5.appendChild(c2);
    }
    w.appendChild(z5);

    // Code, Variablen, Aufrufstapel
    this.unten = el("div", "sl-unten");
    this.codeEl = el("pre", "sl-code");
    var rechts = el("div");
    this.varsEl = el("div", "sl-kasten");
    this.stapelEl = el("div", "sl-kasten sl-stapel");
    rechts.appendChild(this.varsEl);
    rechts.appendChild(this.stapelEl);
    this.unten.appendChild(this.codeEl);
    this.unten.appendChild(rechts);
    if (this.mitCode) w.appendChild(this.unten);
  };

  Labor.prototype.knopf = function (zeile, text, fn, klasse) {
    var b = el("button", klasse || null, text);
    b.type = "button";
    b.addEventListener("click", fn);
    zeile.appendChild(b);
    return b;
  };

  Labor.prototype.uebernehmen = function () {
    this.fehler.textContent = "";
    if (this.verfahren === "mergeteil") {
      var l = liesListe(this.eingabeL.value), r = liesListe(this.eingabeR.value);
      if (!l || !r || !l.length || !r.length) { this.fehler.textContent = "Bitte zwei Listen mit ganzen Zahlen eingeben."; return; }
      if (l.length + r.length > 14) { this.fehler.textContent = "Höchstens 14 Zahlen zusammen."; return; }
      var hinweis = "";
      if (l.join() !== sortiertKopie(l).join() || r.join() !== sortiertKopie(r).join()) {
        l = sortiertKopie(l); r = sortiertKopie(r);
        hinweis = "merge braucht sortierte Listen – sie wurden sortiert.";
      }
      this.links = l; this.rechts = r;
      this.neu();
      this.fehler.textContent = hinweis;
      return;
    }
    var liste = liesListe(this.eingabe.value);
    var max = GRENZE[this.verfahren] || 20;
    if (!liste || liste.length < 2) { this.fehler.textContent = "Bitte mindestens zwei ganze Zahlen eingeben, z. B. 7, 3, 9, 1."; return; }
    if (liste.length > max) { this.fehler.textContent = "Höchstens " + max + " Zahlen, sonst wird es zu eng."; return; }
    for (var k = 0; k < liste.length; k++) {
      if (Math.abs(liste[k]) > 999) { this.fehler.textContent = "Bitte nur Zahlen von −999 bis 999."; return; }
    }
    this.liste = liste;
    this.neu();
  };

  Labor.prototype.neu = function () {
    this.stopp();
    this.antworten = {};
    var v = this.verfahren;
    if (v === "mergeteil") {
      this.eingabeL.value = this.links.join(", ");
      this.eingabeR.value = this.rechts.join(", ");
    } else {
      if (this.liste.length > (GRENZE[v] || 20)) this.liste = this.liste.slice(0, GRENZE[v]);
      this.eingabe.value = this.liste.join(", ");
    }
    if (v === "bubble") this.spur = spurBubble(this.liste);
    else if (v === "insertion") this.spur = spurInsertion(this.liste);
    else if (v === "selection") this.spur = spurSelection(this.liste);
    else if (v === "mergeteil") this.spur = spurMergeTeil(this.links, this.rechts);
    else if (v === "merge") this.spur = spurMerge(this.liste);
    else if (v === "quick") this.spur = spurQuick(this.liste, this.pivotwahl);
    else if (v === "quickinplace") this.spur = spurQuickInPlace(this.liste);
    this.code = CODE[v].slice();
    if (v === "quick" && this.pivotwahl === "mitte") this.code[3] = PIVOT_MITTE;
    this.titel.textContent = "Sortierlabor: " + NAMEN[v];
    this.codeZeilen = [];
    this.codeEl.innerHTML = "";
    for (var k = 0; k < this.code.length; k++) {
      var z = el("span", "z");
      var nr = el("span", "nr", String(k + 1));
      z.appendChild(nr);
      var rest = el("span");
      if (window.Prism && Prism.languages && Prism.languages.python) rest.innerHTML = Prism.highlight(this.code[k], Prism.languages.python, "python");
      else rest.textContent = this.code[k];
      z.appendChild(rest);
      this.codeEl.appendChild(z);
      this.codeZeilen.push(z);
    }
    this.legendeBauen();
    this.feldBauen();
    this.sichtbarBerechnen();
    this.pos = 0;
    this.zeichnen(true);
  };

  Labor.prototype.legendeBauen = function () {
    var v = this.verfahren, eintraege = [];
    if (v === "bubble" || v === "insertion" || v === "selection" || v === "quickinplace") eintraege.push(["#fde68a", "wird verglichen"], ["#fecaca", "wird getauscht"]);
    if (v === "insertion") eintraege.push(["#86efac", "sortierter Teil"]);
    if (v === "selection") eintraege.push(["#1d4ed8", "bisheriges Minimum"]);
    if (v === "quickinplace") eintraege.push(["#e9d5ff", "Pivot"], ["#60a5fa", "kleiner als Pivot"], ["#fdba74", "nicht kleiner"]);
    if (v === "bubble" || v === "selection" || v === "quickinplace" || v === "insertion") eintraege.push(["#bbf7d0", "steht endgültig"]);
    if (v === "merge") eintraege.push(["#ffffff", "noch unsortiert"], ["#f8fafc", "geteilt (wartet)"], ["#fffbeb", "wird zusammengeführt"], ["#dcfce7", "sortiert"]);
    if (v === "quick") eintraege.push(["#ffffff", "noch unsortiert"], ["#e9d5ff", "Pivot (steht fest)"], ["#f8fafc", "aufgeteilt (wartet)"], ["#dcfce7", "sortiert"]);
    if (BAUM[v]) eintraege.push(["#ffffff", "blauer Rahmen: aktiver Aufruf"]);
    this.legende.innerHTML = "";
    for (var k = 0; k < eintraege.length; k++) {
      var s = el("span");
      var i = el("i");
      i.style.background = eintraege[k][0];
      s.appendChild(i);
      s.appendChild(document.createTextNode(eintraege[k][1]));
      this.legende.appendChild(s);
    }
  };

  Labor.prototype.feldBauen = function () {
    var v = this.verfahren;
    this.buehne.innerHTML = "";
    this.elemente = {};
    this.zeigerEl = {};
    if (v === "mergeteil") { this.buehne.style.display = "none"; return; }
    this.buehne.style.display = "";
    if (BAUM[v]) { this.buehne.className = "sl-baum"; return; }
    this.buehne.className = "sl-buehne";
    var liste = this.liste, min = Math.min.apply(null, liste), max = Math.max.apply(null, liste);
    this.indexEl = [];
    for (var k = 0; k < liste.length; k++) {
      var e = el("div", "sl-el");
      var b = el("div", "sl-balken");
      var anteil = max === min ? 0.5 : (liste[k] - min) / (max - min);
      b.style.height = Math.round(14 + anteil * 96) + "px";
      e.appendChild(b);
      e.appendChild(el("div", "sl-karte", String(liste[k])));
      this.buehne.appendChild(e);
      this.elemente[k] = e;
      var ix = el("div", "sl-index", String(k));
      this.buehne.appendChild(ix);
      this.indexEl.push(ix);
    }
    this.buehne.style.height = (110 + 10 + 90) + "px";
  };

  Labor.prototype.sichtbarBerechnen = function () {
    var alt = this.sichtbar ? this.sichtbar[this.pos] : 0;
    this.sichtbar = [];
    for (var k = 0; k < this.spur.length; k++) {
      if (!this.spur[k].fein || this.fein) this.sichtbar.push(k);
    }
    // nächsten sichtbaren Zustand zum bisherigen suchen
    var p = 0;
    for (var m = 0; m < this.sichtbar.length; m++) { if (this.sichtbar[m] <= alt) p = m; }
    this.pos = p;
  };

  Labor.prototype.offeneFrage = function () {
    var z = this.spur[this.sichtbar[this.pos]];
    return this.vorhersage && z.frage && this.antworten[this.sichtbar[this.pos]] === undefined;
  };

  Labor.prototype.schritt = function (r) {
    if (r > 0 && this.offeneFrage()) return;
    var p = this.pos + r;
    if (p < 0 || p >= this.sichtbar.length) return;
    this.pos = p;
    this.zeichnen();
  };
  Labor.prototype.geheZu = function (p) { this.pos = p; this.zeichnen(); };

  Labor.prototype.spielen = function () {
    var self = this;
    if (this.timer) { this.stopp(); return; }
    if (this.pos >= this.sichtbar.length - 1) this.pos = 0;
    this.bSpielen.textContent = "❚❚ Pause";
    function tick() {
      if (self.offeneFrage() || self.pos >= self.sichtbar.length - 1) { self.stopp(); self.zeichnen(); return; }
      self.pos++;
      self.zeichnen();
      self.timer = setTimeout(tick, self.dauer());
    }
    this.timer = setTimeout(tick, 150);
  };
  Labor.prototype.dauer = function () { return Math.round(2200 / Number(this.tempo.value)); };
  Labor.prototype.stopp = function () {
    if (this.timer) clearTimeout(this.timer);
    this.timer = null;
    if (this.bSpielen) this.bSpielen.textContent = "▶▶ Abspielen";
  };

  Labor.prototype.antworten_ = function (idx, wahl) {
    this.antworten[idx] = wahl;
    this.zeichnen();
  };

  Labor.prototype.zeichnen = function (sofort) {
    var self = this;
    var idx = this.sichtbar[this.pos], z = this.spur[idx];
    var frageOffen = this.offeneFrage();
    var v = this.verfahren;

    // Bühne
    if (v !== "mergeteil") {
      if (BAUM[v]) this.baumZeichnen(z, frageOffen);
      else this.feldZeichnen(z, sofort, frageOffen);
    }
    this.panelZeichnen(z, frageOffen);

    // Meldung und Frage
    var m = this.meldung;
    m.innerHTML = "";
    m.className = "sl-meldung";
    var antwort = this.antworten[idx];
    if (frageOffen) {
      m.className = "sl-meldung frage";
      m.appendChild(el("div", null, "Was passiert jetzt? " + z.frage.text));
      var box = el("div", "sl-antworten");
      for (var k = 0; k < z.frage.optionen.length; k++) {
        (function (k) {
          var b = el("button", null, z.frage.optionen[k]);
          b.type = "button";
          b.addEventListener("click", function () { self.antworten_(idx, k); });
          box.appendChild(b);
        })(k);
      }
      m.appendChild(box);
    } else if (this.vorhersage && z.frage && antwort !== undefined) {
      var ok = antwort === z.frage.richtig;
      m.className = "sl-meldung " + (ok ? "richtig" : "falsch");
      m.appendChild(el("div", null, (ok ? "Richtig! " : "Leider nicht – richtig ist „" + z.frage.optionen[z.frage.richtig] + "“. ") + z.frage.erkl));
      m.appendChild(el("div", "sl-info", z.text));
    } else {
      m.textContent = z.text;
    }

    // Steuerung
    this.bZurueck.disabled = this.pos === 0;
    this.bAnfang.disabled = this.pos === 0;
    this.bWeiter.disabled = frageOffen || this.pos >= this.sichtbar.length - 1;

    // Infozeile
    var info = "Schritt <b>" + (this.pos + 1) + "</b> von " + this.sichtbar.length;
    var zeigeV = z.v, zeigeT = z.t;
    if (frageOffen && zeigeV > 0) zeigeV = zeigeV;   // der Vergleich läuft gerade
    info += " · Vergleiche: <b>" + zeigeV + "</b>";
    if (v === "bubble" || v === "insertion" || v === "selection" || v === "quickinplace") info += " · Vertauschungen: <b>" + zeigeT + "</b>";
    var gestellt = 0, richtig = 0;
    for (var a in this.antworten) { gestellt++; if (this.antworten[a] === this.spur[a].frage.richtig) richtig++; }
    if (gestellt) info += " · Vorhersagen richtig: <b>" + richtig + "</b> von " + gestellt;
    this.info.innerHTML = info;

    // Code und Variablen
    if (this.mitCode) {
      for (var c = 0; c < this.codeZeilen.length; c++) this.codeZeilen[c].classList.toggle("an", c + 1 === z.zeile);
      var t = "<h4>Variablen</h4><table>";
      var vorher = this.pos > 0 ? this.spur[this.sichtbar[this.pos - 1]].vars : [];
      for (var r = 0; r < z.vars.length; r++) {
        var geaendert = true;
        for (var q = 0; q < vorher.length; q++) { if (vorher[q][0] === z.vars[r][0] && String(vorher[q][1]) === String(z.vars[r][1])) geaendert = false; }
        t += "<tr" + (geaendert && this.pos > 0 ? " class=\"neu\"" : "") + "><td>" + z.vars[r][0] + "</td><td>" + String(z.vars[r][1]).replace(/</g, "&lt;") + "</td></tr>";
      }
      t += "</table>";
      this.varsEl.innerHTML = t;
      if (z.stapel) {
        this.stapelEl.style.display = "";
        var s = "<h4>Aufrufstapel (oben: läuft gerade)</h4>";
        for (var u = z.stapel.length - 1; u >= 0; u--) s += "<div>" + z.stapel[u] + "</div>";
        this.stapelEl.innerHTML = s;
      } else {
        this.stapelEl.style.display = "none";
      }
    }
  };

  Labor.prototype.feldZeichnen = function (z, sofort, frageOffen) {
    var n = z.ordnung.length;
    var breite = this.buehne.clientWidth || 600;
    var slot = Math.min(64, Math.floor((breite - 16) / n));
    var x0 = Math.round((breite - slot * n) / 2);
    var hl = z.hl || {};
    function drin(liste, k) { return liste && liste.indexOf(k) >= 0; }
    function imBereich(b, k) { return b && k >= b[0] && k < b[1]; }
    for (var k = 0; k < n; k++) {
      var id = z.ordnung[k], e = this.elemente[id];
      if (sofort) e.style.transition = "none";
      e.style.left = (x0 + k * slot) + "px";
      e.style.width = slot + "px";
      if (sofort) { void e.offsetWidth; e.style.transition = ""; }
      var kl = "sl-el";
      if (z.fertig[k]) kl += " fertig";
      else if (imBereich(hl.teil, k)) kl += " teil";
      if (imBereich(hl.klein, k)) kl += " klein";
      if (imBereich(hl.gross, k)) kl += " gross";
      if (drin(hl.pivot, k)) kl += " pivot";
      if (drin(hl.minimum, k)) kl += " minimum";
      if (drin(hl.aktiv, k)) kl += " aktiv";
      if (drin(hl.vergleich, k)) kl += " vergleich";
      if (drin(hl.tausch, k) && !frageOffen) kl += " tausch";
      if (hl.bereich && (k < hl.bereich[0] || k > hl.bereich[1]) && !z.fertig[k]) kl += " aus";
      e.className = kl;
      this.indexEl[k].style.left = (x0 + k * slot) + "px";
      this.indexEl[k].style.width = slot + "px";
    }
    // Zeiger
    for (var name in this.zeigerEl) this.zeigerEl[name].style.display = "none";
    var zeiger = z.zeiger || [], belegt = {};
    for (var p = 0; p < zeiger.length; p++) {
      var zg = zeiger[p], ze = this.zeigerEl[zg.name];
      if (!ze) {
        ze = el("div", "sl-zeiger z" + (Object.keys(this.zeigerEl).length % 3), zg.name);
        this.buehne.appendChild(ze);
        this.zeigerEl[zg.name] = ze;
      }
      var reihe = belegt[zg.pos] || 0;
      belegt[zg.pos] = reihe + 1;
      ze.style.display = "";
      ze.style.left = (x0 + zg.pos * slot + slot / 2 - ze.offsetWidth / 2) + "px";
      ze.style.bottom = (reihe > 0 ? 1 : 19) + "px";   // zweiter Zeiger auf derselben Stelle eine Reihe tiefer
    }
  };

  Labor.prototype.baumZeichnen = function (z, frageOffen) {
    var b = this.buehne, knoten = z.baum || [];
    b.innerHTML = "";
    var n = this.liste.length;
    var breite = b.clientWidth || 600;
    var slot = Math.min(56, Math.floor((breite - 40) / n));
    var x0 = Math.round((breite - slot * n) / 2);
    var zeilenH = 40, tiefeMax = 0;
    for (var k = 0; k < knoten.length; k++) tiefeMax = Math.max(tiefeMax, knoten[k].tiefe);
    b.style.height = ((tiefeMax + 1) * zeilenH + 10) + "px";
    for (var t = 0; t <= tiefeMax; t++) {
      var eb = el("div", "sl-ebene", "Ebene " + t);
      eb.style.top = (t * zeilenH + 14) + "px";
      b.appendChild(eb);
    }
    for (var m = 0; m < knoten.length; m++) {
      var kn = knoten[m];
      var d = el("div", "sl-knoten " + kn.status + (m === z.aktiv ? " aktiv" : ""));
      d.style.left = (x0 + kn.von * slot + 2) + "px";
      d.style.width = ((kn.bis - kn.von) * slot - 4) + "px";
      d.style.top = (kn.tiefe * zeilenH + 6) + "px";
      d.style.height = (zeilenH - 12) + "px";
      var anzahl = kn.bis - kn.von;
      for (var w = 0; w < anzahl; w++) {
        var s;
        if (w < kn.werte.length) {
          s = el("span", null, String(kn.werte[w]));
          if (kn.markiert === w) s.className = "mark";
          if (kn.pivotPos === w && kn.status !== "sortiert") s.className += " piv";
        } else {
          s = el("span", "leer", "0");
        }
        d.appendChild(s);
      }
      b.appendChild(d);
    }
  };

  Labor.prototype.panelZeichnen = function (z, frageOffen) {
    var p = z.panel, box = this.panelEl;
    box.innerHTML = "";
    if (!p) { box.style.display = "none"; return; }
    box.style.display = "";
    function reihe(label) {
      var r = el("div", "sl-reihe");
      r.appendChild(el("span", "lab", label));
      box.appendChild(r);
      return r;
    }
    function karte(r, wert, klasse, pfeil) {
      var k = el("span", "sl-mk" + (klasse ? " " + klasse : ""), String(wert));
      if (pfeil) k.appendChild(el("span", "pf", pfeil));
      r.appendChild(k);
    }
    if (p.typ === "merge") {
      var rl = reihe("links");
      for (var a = 0; a < p.links.length; a++) karte(rl, p.links[a], a < p.i ? "weg" : (a === p.i && p.vergleich ? "vorn" : ""), a === p.i ? "↑ i" : "");
      if (!p.links.length) rl.appendChild(el("span", "sl-leer", "leer"));
      var rr = reihe("rechts");
      for (var b = 0; b < p.rechts.length; b++) karte(rr, p.rechts[b], b < p.j ? "weg" : (b === p.j && p.vergleich ? "vorn" : ""), b === p.j ? "↑ j" : "");
      if (!p.rechts.length) rr.appendChild(el("span", "sl-leer", "leer"));
      var re = reihe("ergebnis");
      for (var c = 0; c < p.ergebnis.length; c++) karte(re, p.ergebnis[c], (p.neu && c === p.ergebnis.length - 1) || p.fertig ? "neu" : "");
      if (!p.ergebnis.length) re.appendChild(el("span", "sl-leer", "noch leer"));
    } else if (p.typ === "partition") {
      var rp = reihe("Pivot");
      karte(rp, p.pivot, "piv");
      if (p.x !== undefined) {
        rp.appendChild(el("span", "sl-info", "  gerade dran: x = "));
        karte(rp, p.x, "vorn");
      }
      var namen = [["kleiner", p.kleiner], ["gleich", p.gleich], ["groesser", p.groesser]];
      for (var q = 0; q < 3; q++) {
        var r = reihe(namen[q][0]);
        for (var s = 0; s < namen[q][1].length; s++) karte(r, namen[q][1][s], q === 1 ? "piv" : "");
        if (!namen[q][1].length) r.appendChild(el("span", "sl-leer", "leer"));
      }
    }
  };

  /* ---------- Wettrennen: alle Verfahren gleichzeitig ---------- */
  // Jedes Verfahren liefert eine Folge von Ereignissen: v = Vergleich, s = Tausch, w = Schreiben
  function opsBubble(a) {
    var ops = [], n = a.length;
    for (var d = 0; d < n - 1; d++) {
      var getauscht = false;
      for (var j = 0; j < n - 1 - d; j++) {
        ops.push(["v", j, j + 1]);
        if (a[j] > a[j + 1]) { var x = a[j]; a[j] = a[j + 1]; a[j + 1] = x; ops.push(["s", j, j + 1]); getauscht = true; }
      }
      if (!getauscht) break;
    }
    return ops;
  }
  function opsInsertion(a) {
    var ops = [];
    for (var i = 1; i < a.length; i++) {
      var j = i;
      while (j > 0) {
        ops.push(["v", j - 1, j]);
        if (a[j - 1] > a[j]) { var x = a[j]; a[j] = a[j - 1]; a[j - 1] = x; ops.push(["s", j - 1, j]); j--; }
        else break;
      }
    }
    return ops;
  }
  function opsSelection(a) {
    var ops = [], n = a.length;
    for (var i = 0; i < n - 1; i++) {
      var m = i;
      for (var j = i + 1; j < n; j++) { ops.push(["v", j, m]); if (a[j] < a[m]) m = j; }
      if (m !== i) { var x = a[i]; a[i] = a[m]; a[m] = x; ops.push(["s", i, m]); }
    }
    return ops;
  }
  function opsMerge(a) {
    var ops = [];
    function ms(von, bis) {
      if (bis - von <= 1) return;
      var mitte = von + Math.floor((bis - von) / 2);
      ms(von, mitte); ms(mitte, bis);
      var L = a.slice(von, mitte), R = a.slice(mitte, bis), i = 0, j = 0, k = von;
      while (i < L.length && j < R.length) {
        ops.push(["v", von + i, mitte + j]);
        if (L[i] <= R[j]) { a[k] = L[i]; i++; } else { a[k] = R[j]; j++; }
        ops.push(["w", k, a[k]]); k++;
      }
      while (i < L.length) { a[k] = L[i]; ops.push(["w", k, a[k]]); i++; k++; }
      while (j < R.length) { a[k] = R[j]; ops.push(["w", k, a[k]]); j++; k++; }
    }
    ms(0, a.length);
    return ops;
  }
  function opsQuick(a) {
    var ops = [];
    function qs(links, rechts) {
      if (!(links < rechts)) return;
      var pivot = a[rechts], grenze = links;
      for (var j = links; j < rechts; j++) {
        ops.push(["v", j, rechts]);
        if (a[j] < pivot) {
          if (grenze !== j) { var x = a[grenze]; a[grenze] = a[j]; a[j] = x; ops.push(["s", grenze, j]); }
          grenze++;
        }
      }
      if (grenze !== rechts) { var y = a[grenze]; a[grenze] = a[rechts]; a[rechts] = y; ops.push(["s", grenze, rechts]); }
      qs(links, grenze - 1);
      qs(grenze + 1, rechts);
    }
    qs(0, a.length - 1);
    return ops;
  }
  var RENNER = [
    ["Bubblesort", opsBubble], ["Insertionsort", opsInsertion], ["Selectionsort", opsSelection],
    ["Mergesort", opsMerge], ["Quicksort", opsQuick]
  ];
  function zaehleVergleiche(fn, liste) {
    var ops = fn(liste.slice()), v = 0;
    for (var k = 0; k < ops.length; k++) if (ops[k][0] === "v") v++;
    return v;
  }
  function startliste(art, n) {
    var a = [];
    for (var k = 1; k <= n; k++) a.push(k);
    if (art === "sortiert") return a;
    if (art === "absteigend") return a.reverse();
    if (art === "fast") {
      for (var m = 0; m < Math.max(1, Math.floor(n / 10)); m++) {
        var i = Math.floor(Math.random() * (n - 1));
        var x = a[i]; a[i] = a[i + 1]; a[i + 1] = x;
      }
      return a;
    }
    for (var j = n - 1; j > 0; j--) {
      var r = Math.floor(Math.random() * (j + 1));
      var y = a[j]; a[j] = a[r]; a[r] = y;
    }
    return a;
  }

  function Rennen(wurzel) {
    this.w = wurzel;
    this.timer = null;
    this.bauen();
    this.neu();
  }
  Rennen.prototype.bauen = function () {
    var self = this, w = this.w;
    w.innerHTML = "";
    w.classList.add("sl");
    w.appendChild(el("div", "sl-titel", "Wettrennen: Alle Verfahren sortieren dieselbe Liste"));
    var z1 = el("div", "sl-zeile");
    var l1 = el("label", null, "Anzahl n: ");
    this.nSel = el("select");
    var ns = [10, 20, 40, 80];
    for (var k = 0; k < ns.length; k++) { var o = el("option", null, String(ns[k])); o.value = ns[k]; this.nSel.appendChild(o); }
    this.nSel.value = "40";
    l1.appendChild(this.nSel);
    z1.appendChild(l1);
    var l2 = el("label", null, "Startreihenfolge: ");
    this.artSel = el("select");
    var arten = [["zufall", "zufällig"], ["fast", "fast sortiert"], ["sortiert", "schon sortiert"], ["absteigend", "absteigend"]];
    for (var m = 0; m < arten.length; m++) { var o2 = el("option", null, arten[m][1]); o2.value = arten[m][0]; this.artSel.appendChild(o2); }
    l2.appendChild(this.artSel);
    z1.appendChild(l2);
    this.nSel.addEventListener("change", function () { self.neu(); });
    this.artSel.addEventListener("change", function () { self.neu(); });
    w.appendChild(z1);
    var z2 = el("div", "sl-zeile");
    this.bStart = el("button", "haupt", "▶ Start"); this.bStart.type = "button";
    this.bStart.addEventListener("click", function () { self.startStopp(); });
    var bNeu = el("button", null, "Neue Liste"); bNeu.type = "button";
    bNeu.addEventListener("click", function () { self.neu(); });
    z2.appendChild(this.bStart); z2.appendChild(bNeu);
    var tl = el("label", "sl-info", "Tempo ");
    this.tempo = el("input"); this.tempo.type = "range"; this.tempo.min = "1"; this.tempo.max = "10"; this.tempo.value = "6";
    this.tempo.style.width = "6em"; this.tempo.style.verticalAlign = "middle";
    tl.appendChild(this.tempo);
    z2.appendChild(tl);
    w.appendChild(z2);
    w.appendChild(el("div", "sl-info", "Ein Zeittakt = ein Vergleich. Wer weniger vergleicht, ist früher fertig. Gelb: Vergleich, rot: Tausch oder Schreiben."));
    this.gitter = el("div", "sl-rennen-gitter");
    w.appendChild(this.gitter);

    var z3 = el("div", "sl-zeile");
    var bMessen = el("button", null, "Vergleiche für n = 8 bis 512 zählen"); bMessen.type = "button";
    bMessen.addEventListener("click", function () { self.messen(); });
    z3.appendChild(bMessen);
    z3.appendChild(el("span", "sl-info", "(gleiche Startreihenfolge wie oben)"));
    w.appendChild(z3);
    this.messung = el("div");
    w.appendChild(this.messung);
  };
  Rennen.prototype.neu = function () {
    this.stopp();
    var n = Number(this.nSel.value);
    this.basis = startliste(this.artSel.value, n);
    this.bahnen = [];
    this.gitter.innerHTML = "";
    this.takt = 0;
    this.platz = 0;
    for (var k = 0; k < RENNER.length; k++) {
      var a = this.basis.slice();
      var bahn = { name: RENNER[k][0], a: this.basis.slice(), ops: RENNER[k][1](a), p: 0, v: 0, fertig: false };
      var box = el("div", "sl-bahn");
      var h = el("h4");
      h.appendChild(el("span", null, bahn.name));
      bahn.stand = el("span", "sl-info", "0 Vergleiche");
      h.appendChild(bahn.stand);
      box.appendChild(h);
      var f = el("div", "flaeche");
      bahn.saeulen = [];
      for (var m = 0; m < n; m++) { var s = el("div"); f.appendChild(s); bahn.saeulen.push(s); }
      box.appendChild(f);
      bahn.box = box;
      this.gitter.appendChild(box);
      this.bahnen.push(bahn);
      this.malen(bahn, null);
    }
    this.bStart.textContent = "▶ Start";
  };
  Rennen.prototype.malen = function (bahn, markiert) {
    var n = bahn.a.length;
    for (var k = 0; k < n; k++) {
      var s = bahn.saeulen[k];
      s.style.height = Math.round(4 + bahn.a[k] / n * 100) + "px";
      s.className = "";
    }
    if (markiert) {
      var kl = markiert[0] === "v" ? "v" : "s";
      bahn.saeulen[markiert[1]].className = kl;
      if (markiert[0] !== "w") bahn.saeulen[markiert[2]].className = kl;
    }
  };
  Rennen.prototype.taktSchritt = function () {
    var alleFertig = true;
    this.takt++;
    for (var k = 0; k < this.bahnen.length; k++) {
      var b = this.bahnen[k];
      if (b.fertig) continue;
      var letzte = null, vergleich = false;
      while (b.p < b.ops.length) {
        var op = b.ops[b.p];
        if (op[0] === "v") { if (vergleich) break; vergleich = true; b.v++; }
        else if (op[0] === "s") { var x = b.a[op[1]]; b.a[op[1]] = b.a[op[2]]; b.a[op[2]] = x; }
        else if (op[0] === "w") { b.a[op[1]] = op[2]; }
        letzte = op;
        b.p++;
      }
      if (b.p >= b.ops.length) {
        b.fertig = true;
        this.platz++;
        b.box.classList.add("fertig");
        this.malen(b, null);
        b.stand.innerHTML = "<span class=\"sl-platz\">" + this.platz + ". Platz</span> · " + b.v + " Vergleiche";
      } else {
        alleFertig = false;
        this.malen(b, letzte);
        b.stand.textContent = b.v + " Vergleiche";
      }
    }
    return alleFertig;
  };
  Rennen.prototype.startStopp = function () {
    var self = this;
    if (this.timer) { this.stopp(); return; }
    if (this.bahnen.every(function (b) { return b.fertig; })) this.neu();
    this.bStart.textContent = "❚❚ Pause";
    function tick() {
      var takte = Math.max(1, Math.round(Math.pow(1.9, Number(self.tempo.value) - 4)));
      var fertig = false;
      for (var k = 0; k < takte && !fertig; k++) fertig = self.taktSchritt();
      if (fertig) { self.stopp(); self.bStart.textContent = "▶ Start"; return; }
      self.timer = setTimeout(tick, 40);
    }
    tick();
  };
  Rennen.prototype.stopp = function () {
    if (this.timer) clearTimeout(this.timer);
    this.timer = null;
    if (this.bStart) this.bStart.textContent = "▶ Weiter";
  };
  Rennen.prototype.messen = function () {
    var ns = [8, 16, 32, 64, 128, 256, 512], art = this.artSel.value;
    var werte = [];
    for (var k = 0; k < RENNER.length; k++) werte.push([]);
    for (var m = 0; m < ns.length; m++) {
      var liste = startliste(art, ns[m]);
      for (var r = 0; r < RENNER.length; r++) werte[r].push(zaehleVergleiche(RENNER[r][1], liste));
    }
    var t = "<table><thead><tr><th>Verfahren</th>";
    for (var a = 0; a < ns.length; a++) t += "<th>n = " + ns[a] + "</th>";
    t += "<th>Faktor bei Verdopplung (256 → 512)</th></tr></thead><tbody>";
    for (var b = 0; b < RENNER.length; b++) {
      t += "<tr><td>" + RENNER[b][0] + "</td>";
      for (var c = 0; c < ns.length; c++) t += "<td>" + werte[b][c].toLocaleString("de-DE") + "</td>";
      var f = werte[b][ns.length - 2] ? (werte[b][ns.length - 1] / werte[b][ns.length - 2]) : 0;
      t += "<td>≈ " + f.toFixed(1).replace(".", ",") + "</td></tr>";
    }
    t += "</tbody></table>";
    // Liniendiagramm (lineare Achsen)
    var B = 640, H = 300, li = 70, un = 40, ob = 15, re = 120;
    var maxV = 1;
    for (var d = 0; d < werte.length; d++) for (var e = 0; e < ns.length; e++) maxV = Math.max(maxV, werte[d][e]);
    var farben = ["#dc2626", "#d97706", "#7c3aed", "#15803d", "#1d4ed8"];
    function px(n) { return li + (n / 512) * (B - li - re); }
    function py(v) { return H - un - (v / maxV) * (H - un - ob); }
    var svg = "<svg class=\"sl-diagramm\" viewBox=\"0 0 " + B + " " + H + "\" role=\"img\" aria-label=\"Vergleiche in Abhängigkeit von n\">";
    svg += "<line x1=\"" + li + "\" y1=\"" + (H - un) + "\" x2=\"" + (B - re) + "\" y2=\"" + (H - un) + "\" stroke=\"#64748b\"/>";
    svg += "<line x1=\"" + li + "\" y1=\"" + ob + "\" x2=\"" + li + "\" y2=\"" + (H - un) + "\" stroke=\"#64748b\"/>";
    for (var g = 0; g < ns.length; g++) {
      if (ns[g] < 64) continue;
      svg += "<text x=\"" + px(ns[g]) + "\" y=\"" + (H - un + 16) + "\" font-size=\"11\" text-anchor=\"middle\" fill=\"#4b5563\">" + ns[g] + "</text>";
    }
    svg += "<text x=\"" + ((li + B - re) / 2) + "\" y=\"" + (H - 6) + "\" font-size=\"12\" text-anchor=\"middle\" fill=\"#111827\">Anzahl n</text>";
    for (var h = 0; h <= 4; h++) {
      var vv = maxV * h / 4;
      svg += "<text x=\"" + (li - 6) + "\" y=\"" + (py(vv) + 4) + "\" font-size=\"11\" text-anchor=\"end\" fill=\"#4b5563\">" + Math.round(vv).toLocaleString("de-DE") + "</text>";
      if (h > 0) svg += "<line x1=\"" + li + "\" y1=\"" + py(vv) + "\" x2=\"" + (B - re) + "\" y2=\"" + py(vv) + "\" stroke=\"#e5e7eb\"/>";
    }
    svg += "<text x=\"14\" y=\"" + ((ob + H - un) / 2) + "\" font-size=\"12\" fill=\"#111827\" transform=\"rotate(-90 14 " + ((ob + H - un) / 2) + ")\" text-anchor=\"middle\">Vergleiche</text>";
    for (var q = 0; q < RENNER.length; q++) {
      var pfad = "";
      for (var s = 0; s < ns.length; s++) pfad += (s ? " L " : "M ") + px(ns[s]).toFixed(1) + " " + py(werte[q][s]).toFixed(1);
      svg += "<path d=\"" + pfad + "\" fill=\"none\" stroke=\"" + farben[q] + "\" stroke-width=\"2.2\"/>";
      var yEnde = py(werte[q][ns.length - 1]);
      svg += "<text x=\"" + (B - re + 6) + "\" y=\"" + (yEnde + 4 + (q === 4 ? 10 : 0) - (q === 3 ? 2 : 0)) + "\" font-size=\"11\" fill=\"" + farben[q] + "\">" + RENNER[q][0] + "</text>";
    }
    svg += "</svg>";
    this.messung.innerHTML = t + svg;
  };

  /* ---------- Hochrechner: aus einer Messung auf große n schließen ---------- */
  var KLASSEN = [
    ["n", "O(n)", function (n) { return n; }],
    ["nlogn", "O(n · log n)", function (n) { return n * Math.log(n) / Math.LN2; }],
    ["n2", "O(n²)", function (n) { return n * n; }],
    ["logn", "O(log n)", function (n) { return Math.log(n) / Math.LN2; }]
  ];
  function dauerText(s) {
    function z(x, st) { return x.toLocaleString("de-DE", { maximumFractionDigits: st }); }
    if (s < 0.001) return z(s * 1e6, 1) + " µs";
    if (s < 1) return z(s * 1000, 1) + " ms";
    if (s < 120) return z(s, 2) + " s";
    if (s < 7200) return z(s / 60, 1) + " Minuten";
    if (s < 172800) return z(s / 3600, 1) + " Stunden";
    if (s < 63072000) return z(s / 86400, 1) + " Tage";
    return z(s / 31557600, 1) + " Jahre";
  }
  function Hochrechner(wurzel) {
    var self = this;
    this.w = wurzel;
    wurzel.innerHTML = "";
    wurzel.classList.add("sl");
    wurzel.appendChild(el("div", "sl-titel", "Hochrechner: Wie lange dauert es für viel mehr Daten?"));
    function feld(label, wert, breite) {
      var l = el("label", null, label + " ");
      var i = el("input"); i.type = "text"; i.value = wert; i.style.width = breite || "7em";
      i.addEventListener("input", function () { self.rechnen(); });
      l.appendChild(i);
      return [l, i];
    }
    var z1 = el("div", "sl-zeile");
    z1.appendChild(el("b", null, "Messung:"));
    var d = wurzel.dataset;
    var a = feld("n =", d.n || "4000"); this.n1 = a[1]; z1.appendChild(a[0]);
    var b = feld("Zeit in s =", d.zeit || "1,92"); this.t1 = b[1]; z1.appendChild(b[0]);
    wurzel.appendChild(z1);
    var z2 = el("div", "sl-zeile");
    z2.appendChild(el("b", null, "Annahme:"));
    var lk = el("label", null, "Das Verfahren liegt in ");
    this.klasse = el("select");
    for (var k = 0; k < KLASSEN.length; k++) { var o = el("option", null, KLASSEN[k][1]); o.value = KLASSEN[k][0]; this.klasse.appendChild(o); }
    this.klasse.value = d.klasse || "n2";
    this.klasse.addEventListener("change", function () { self.rechnen(); });
    lk.appendChild(this.klasse);
    z2.appendChild(lk);
    wurzel.appendChild(z2);
    var z3 = el("div", "sl-zeile");
    z3.appendChild(el("b", null, "Gesucht:"));
    var c = feld("n =", "100000000", "9em"); this.n2 = c[1]; z3.appendChild(c[0]);
    wurzel.appendChild(z3);
    var z4 = el("div", "sl-zeile");
    z4.appendChild(el("span", "sl-info", "Schnell einsetzen:"));
    var ziele = [["eigene Playlist", 2000], ["Songliste im Kurs", 50000], ["ganzer Streamingdienst", 100000000]];
    for (var m = 0; m < ziele.length; m++) {
      (function (zl) {
        var bt = el("button", null, zl[0] + " (" + zl[1].toLocaleString("de-DE") + ")"); bt.type = "button";
        bt.addEventListener("click", function () { self.n2.value = String(zl[1]); self.rechnen(); });
        z4.appendChild(bt);
      })(ziele[m]);
    }
    wurzel.appendChild(z4);
    this.ausgabe = el("div", "sl-meldung");
    wurzel.appendChild(this.ausgabe);
    this.rechnen();
  }
  Hochrechner.prototype.rechnen = function () {
    function zahl(t) {
      // „0,82“ und „0.82“ sind beide erlaubt; „100.000.000“ mit Tausenderpunkten auch
      var s = String(t).replace(/\s/g, "");
      if (s.indexOf(",") >= 0 || (s.match(/\./g) || []).length > 1 || /^\d{1,3}\.\d{3}$/.test(s)) s = s.replace(/\./g, "").replace(",", ".");
      return Number(s);
    }
    var n1 = zahl(this.n1.value), t1 = zahl(this.t1.value), n2 = zahl(this.n2.value);
    if (!(n1 > 1) || !(t1 > 0) || !(n2 > 1)) { this.ausgabe.textContent = "Bitte positive Zahlen eingeben (n größer als 1)."; return; }
    var f = KLASSEN[0][2], name = "";
    for (var k = 0; k < KLASSEN.length; k++) if (KLASSEN[k][0] === this.klasse.value) { f = KLASSEN[k][2]; name = KLASSEN[k][1]; }
    var faktor = f(n2) / f(n1);
    var t2 = t1 * faktor;
    this.ausgabe.innerHTML = "";
    this.ausgabe.appendChild(el("div", null, "Vorhersage für n = " + n2.toLocaleString("de-DE") + ": etwa " + dauerText(t2)));
    this.ausgabe.firstChild.style.fontWeight = "bold";
    this.ausgabe.appendChild(el("div", "sl-info", "Rechenweg: Bei " + name + " wächst der Aufwand von n = " + n1.toLocaleString("de-DE") + " auf n = " +
      n2.toLocaleString("de-DE") + " um den Faktor " + faktor.toLocaleString("de-DE", { maximumSignificantDigits: 3 }) + ". " +
      dauerText(t1) + " · " + faktor.toLocaleString("de-DE", { maximumSignificantDigits: 3 }) + " ≈ " + dauerText(t2) + ". Das ist eine Schätzung: Sie stimmt nur, wenn die Annahme über die Klasse stimmt und n groß genug ist."));
  };

  /* ---------- Start ---------- */
  function los() {
    var orte = document.querySelectorAll("div.sortierlabor");
    if (!orte.length) return;
    stil();
    for (var k = 0; k < orte.length; k++) {
      try {
        if (orte[k].dataset.verfahren === "rennen") new Rennen(orte[k]);
        else if (orte[k].dataset.verfahren === "hochrechner") new Hochrechner(orte[k]);
        else new Labor(orte[k]);
      } catch (fehler) {
        orte[k].textContent = "Das Sortierlabor konnte nicht starten: " + fehler.message;
      }
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", los);
  else los();
})();

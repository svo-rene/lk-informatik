/* seite.js – Bedienung der Kurswebseite
   - Hell/Dunkel-Schalter (Wahl bleibt im Browser gespeichert)
   - Menü auf dem Handy, Themensuche in der Seitenleiste
   - Anker an Überschriften und Inhaltsverzeichnis rechts mit Mitlauf-Markierung
   - Code: Kopieren für alle Blöcke, Ausführen/Bearbeiten für <pre class="ausfuehrbar"> mit Natter
*/
(function () {
    "use strict";
    var NATTER = "https://cdn.jsdelivr.net/npm/@natterjs/web@0.1.2/dist/natter-web.js";
    var root = document.body.getAttribute("data-root") || "";

    function speichern(k, v) { try { localStorage.setItem(k, v); } catch (e) { } }

    /* ---------- Hell / dunkel ---------- */
    var themaKnopf = document.getElementById("thema-knopf");
    if (themaKnopf) {
        themaKnopf.addEventListener("click", function () {
            var html = document.documentElement;
            var jetzt = html.getAttribute("data-theme");
            if (!jetzt) jetzt = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
            var neu = jetzt === "dark" ? "light" : "dark";
            html.setAttribute("data-theme", neu);
            speichern("thema", neu);
        });
    }

    /* ---------- Menü und Seitenleiste ---------- */
    var leiste = document.getElementById("leiste");
    var menue = document.getElementById("menue-knopf");
    if (menue && leiste) {
        menue.addEventListener("click", function () {
            var offen = leiste.classList.toggle("offen");
            menue.setAttribute("aria-expanded", offen ? "true" : "false");
        });
        document.addEventListener("keydown", function (ev) {
            if (ev.key === "Escape") { leiste.classList.remove("offen"); menue.setAttribute("aria-expanded", "false"); }
        });
    }
    var aktiv = leiste && leiste.querySelector("a.aktiv");
    if (aktiv) {
        var r = aktiv.getBoundingClientRect();
        if (r.bottom > window.innerHeight - 40) leiste.scrollTop += r.top - window.innerHeight / 2;
    }

    var filter = document.getElementById("filter");
    if (filter && leiste) {
        filter.addEventListener("input", function () {
            var q = filter.value.trim().toLowerCase();
            var bereiche = leiste.querySelectorAll("details.lb");
            for (var i = 0; i < bereiche.length; i++) {
                var b = bereiche[i], treffer = 0;
                var eintraege = b.querySelectorAll("li");
                for (var j = 0; j < eintraege.length; j++) {
                    var passt = !q || eintraege[j].textContent.toLowerCase().indexOf(q) >= 0;
                    eintraege[j].classList.toggle("versteckt", !passt);
                    if (passt) treffer++;
                }
                var kaps = b.querySelectorAll(".kap");
                for (var k = 0; k < kaps.length; k++) {
                    var ul = kaps[k].nextElementSibling;
                    kaps[k].classList.toggle("versteckt", !!q && !(ul && ul.querySelector("li:not(.versteckt)")));
                }
                b.classList.toggle("versteckt", !!q && treffer === 0);
                if (q) b.open = treffer > 0;
            }
        });
    }

    /* ---------- Überschriften: Anker und Inhaltsverzeichnis ---------- */
    var inhalt = document.querySelector(".seiteninhalt");
    var toc = document.getElementById("toc");
    function slug(t) {
        return t.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
            .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "abschnitt";
    }
    if (inhalt) {
        var vergeben = {};
        var hs = inhalt.querySelectorAll("h2, h3");
        var liste = [];
        for (var h = 0; h < hs.length; h++) {
            var el = hs[h];
            if (el.closest("details, .aufgabe, .beispiel, .merke, .hinweis")) continue;
            if (!el.id) {
                var id = slug(el.textContent), n = 2, basis = id;
                while (vergeben[id] || document.getElementById(id)) id = basis + "-" + n++;
                el.id = id;
            }
            vergeben[el.id] = true;
            var a = document.createElement("a");
            a.className = "anker";
            a.href = "#" + el.id;
            a.setAttribute("aria-label", "Link zu diesem Abschnitt");
            a.textContent = "#";
            el.appendChild(a);
            liste.push(el);
        }
        if (toc && liste.length >= 2) {
            var html = '<p class="toc-titel">Auf dieser Seite</p><ul>';
            for (var t = 0; t < liste.length; t++) {
                var text = liste[t].firstChild ? liste[t].textContent.replace(/#$/, "").trim() : "";
                html += '<li><a href="#' + liste[t].id + '"' + (liste[t].tagName === "H3" ? ' class="unter"' : "") + ">" +
                    text.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</a></li>";
            }
            toc.innerHTML = html + "</ul>";
            var links = toc.querySelectorAll("a");
            var markiere = function () {
                var y = window.scrollY + 200, akt = 0;
                for (var i = 0; i < liste.length; i++) if (liste[i].getBoundingClientRect().top + window.scrollY <= y) akt = i;
                for (var j = 0; j < links.length; j++) links[j].classList.toggle("aktiv", j === akt);
            };
            window.addEventListener("scroll", markiere, { passive: true });
            markiere();
        } else if (toc) {
            toc.remove();
            document.body.classList.remove("mit-toc");
        }
    }

    /* Sprung zu einer Aufgabe: gleich aufklappen */
    function aufklappen() {
        if (!location.hash) return;
        var ziel = document.getElementById(decodeURIComponent(location.hash.slice(1)));
        if (!ziel) return;
        var det = ziel.tagName === "DETAILS" ? ziel : ziel.querySelector("details");
        if (det) det.open = true;
        var p = ziel.parentElement;
        while (p) { if (p.tagName === "DETAILS") p.open = true; p = p.parentElement; }
    }
    window.addEventListener("hashchange", aufklappen);
    aufklappen();

    /* ---------- Code-Blöcke ---------- */
    var SVG = {
        kopie: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',
        start: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4v16l13-8z"/></svg>',
        stift: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4z"/></svg>',
        zurueck: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
        stopp: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="1"/></svg>'
    };
    function knopf(cls, svg, text, titel) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "code-knopf " + cls;
        b.innerHTML = svg + "<span>" + text + "</span>";
        if (titel) b.title = titel;
        return b;
    }
    var natter = null;
    function ladeNatter() {
        if (!natter) natter = import(NATTER);
        return natter;
    }

    var bloecke = document.querySelectorAll(".seiteninhalt pre");
    for (var i = 0; i < bloecke.length; i++) {
        (function (pre) {
            if (pre.closest(".sortierlabor, .zw-panel") || pre.classList.contains("schema")) return;
            var code = pre.querySelector("code") || pre;
            var huelle = document.createElement("div");
            huelle.className = "code-block";
            pre.parentNode.insertBefore(huelle, pre);
            huelle.appendChild(pre);
            var werkzeuge = document.createElement("div");
            werkzeuge.className = "code-werkzeuge";
            huelle.appendChild(werkzeuge);

            var kopie = knopf("", SVG.kopie, "Kopieren", "Code kopieren");
            kopie.addEventListener("click", function () {
                var fertig = function () {
                    kopie.querySelector("span").textContent = "Kopiert";
                    setTimeout(function () { kopie.querySelector("span").textContent = "Kopieren"; }, 1500);
                };
                if (navigator.clipboard) navigator.clipboard.writeText(code.textContent).then(fertig);
            });

            if (!pre.classList.contains("ausfuehrbar")) { werkzeuge.appendChild(kopie); return; }
            huelle.classList.add("ausfuehrbar");
            var original = code.textContent;
            var start = knopf("start", SVG.start, "Ausführen", "Programm hier auf der Seite ausführen");
            var bearbeiten = knopf("", SVG.stift, "Ändern", "Code hier auf der Seite ändern");
            var zurueck = knopf("", SVG.zurueck, "Zurück", "Ursprünglichen Code wiederherstellen");
            zurueck.hidden = true;
            werkzeuge.appendChild(bearbeiten);
            werkzeuge.appendChild(zurueck);
            werkzeuge.appendChild(kopie);
            werkzeuge.appendChild(start);

            bearbeiten.addEventListener("click", function () {
                var an = pre.getAttribute("contenteditable") !== "true";
                if (an) {
                    code.textContent = code.textContent;   // Hervorhebung entfernen
                    pre.setAttribute("contenteditable", "true");
                    pre.setAttribute("spellcheck", "false");
                    pre.focus();
                    bearbeiten.querySelector("span").textContent = "Fertig";
                } else {
                    pre.removeAttribute("contenteditable");
                    if (window.Prism) Prism.highlightElement(code);
                    bearbeiten.querySelector("span").textContent = "Ändern";
                }
                zurueck.hidden = false;
            });
            pre.addEventListener("keydown", function (ev) {
                if (pre.getAttribute("contenteditable") !== "true") return;
                if (ev.key === "Tab") { ev.preventDefault(); document.execCommand("insertText", false, "    "); }
                if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); start.click(); }
            });
            zurueck.addEventListener("click", function () {
                pre.removeAttribute("contenteditable");
                code.textContent = original;
                if (window.Prism) Prism.highlightElement(code);
                bearbeiten.querySelector("span").textContent = "Ändern";
                zurueck.hidden = true;
            });

            var ausgabe = null, runner = null, laeuft = false;
            start.addEventListener("click", function () {
                if (laeuft && runner) { runner.stop(); return; }
                if (!ausgabe) {
                    ausgabe = document.createElement("div");
                    ausgabe.className = "code-ausgabe";
                    ausgabe.innerHTML = '<div class="code-ausgabe-kopf">Ausgabe</div><div class="code-konsole"></div>' +
                        '<div class="code-plot"></div><p class="code-hinweis">Läuft mit Natter direkt im Browser. ' +
                        "Zeitmessungen sind hier langsamer als in Thonny.</p>";
                    var zu = knopf("", "", "Schließen");
                    zu.style.cssText = "background:none;border:none;color:inherit";
                    zu.addEventListener("click", function () { if (runner) runner.stop(); ausgabe.remove(); ausgabe = null; });
                    ausgabe.querySelector(".code-ausgabe-kopf").appendChild(zu);
                    huelle.appendChild(ausgabe);
                }
                var konsole = ausgabe.querySelector(".code-konsole");
                konsole.innerHTML = "<em>Python wird geladen …</em>";
                huelle.classList.add("laeuft");
                ladeNatter().then(function (m) {
                    konsole.innerHTML = "";
                    runner = m.createRunner();
                    m.createConsole(konsole, { lang: "de" }).connect(runner);
                    var quelltext = code.textContent;
                    if (m.detectModules(quelltext).indexOf("plot") >= 0) runner.use(m.createPlot(ausgabe.querySelector(".code-plot")));
                    laeuft = true;
                    start.className = "code-knopf";
                    start.innerHTML = SVG.stopp + "<span>Stopp</span>";
                    return runner.run(quelltext);
                }).catch(function (fehler) {
                    konsole.textContent = "Python konnte nicht geladen werden (" + fehler + "). Ist die Internetverbindung da?";
                }).then(function () {
                    laeuft = false;
                    huelle.classList.remove("laeuft");
                    start.className = "code-knopf start";
                    start.innerHTML = SVG.start + "<span>Ausführen</span>";
                });
            });
        })(bloecke[i]);
    }
})();

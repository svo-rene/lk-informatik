/* seite.js – Menü auf dem Handy, Themensuche in der Seitenleiste, aktives Thema sichtbar machen. */
(function () {
    var leiste = document.getElementById("leiste");
    var knopf = document.getElementById("menue-knopf");
    if (knopf && leiste) {
        knopf.addEventListener("click", function () {
            var offen = leiste.classList.toggle("offen");
            knopf.setAttribute("aria-expanded", offen ? "true" : "false");
        });
    }

    // aktives Thema in der Seitenleiste in den sichtbaren Bereich holen
    var aktiv = leiste && leiste.querySelector("a.aktiv");
    if (aktiv && aktiv.scrollIntoView) {
        aktiv.scrollIntoView({ block: "center" });
        window.scrollTo(0, 0);
    }

    // Filter: Themen nach Text suchen
    var filter = document.getElementById("filter");
    if (filter && leiste) {
        filter.addEventListener("input", function () {
            var q = filter.value.trim().toLowerCase();
            var bereiche = leiste.querySelectorAll("details.lb");
            for (var i = 0; i < bereiche.length; i++) {
                var b = bereiche[i];
                var treffer = 0;
                var eintraege = b.querySelectorAll("li");
                for (var j = 0; j < eintraege.length; j++) {
                    var passt = !q || eintraege[j].textContent.toLowerCase().indexOf(q) >= 0;
                    eintraege[j].classList.toggle("versteckt", !passt);
                    if (passt) treffer++;
                }
                var kaps = b.querySelectorAll(".kap");
                for (var k = 0; k < kaps.length; k++) {
                    var ul = kaps[k].nextElementSibling;
                    var sichtbar = ul && ul.querySelector("li:not(.versteckt)");
                    kaps[k].classList.toggle("versteckt", q && !sichtbar);
                }
                b.classList.toggle("versteckt", q && treffer === 0);
                if (q) b.open = treffer > 0;
            }
        });
    }

    // Sprung zu #aufgabe-…: Aufgabe gleich aufklappen
    function aufklappen() {
        if (!location.hash) return;
        var ziel = document.getElementById(decodeURIComponent(location.hash.slice(1)));
        if (!ziel) return;
        var det = ziel.tagName === "DETAILS" ? ziel : ziel.querySelector("details");
        if (det) det.open = true;
    }
    window.addEventListener("hashchange", aufklappen);
    aufklappen();
})();

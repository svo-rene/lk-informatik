-- Onlineshop – Ausgangsdatenbank für Kursseite 1.18, Teil B
-- Drei Relationen sind fertig gefüllt. Die Verbindungsrelation
-- zwischen Bestellung und Produkt fehlt: Sie ist deine Aufgabe.

DROP TABLE IF EXISTS Bestellung;
DROP TABLE IF EXISTS Produkt;
DROP TABLE IF EXISTS Kunde;

CREATE TABLE Kunde (
    KundenNr INTEGER PRIMARY KEY,
    Name     TEXT NOT NULL,
    Ort      TEXT NOT NULL
);

CREATE TABLE Produkt (
    ProduktNr   INTEGER PRIMARY KEY,
    Bezeichnung TEXT NOT NULL,
    Preis       REAL NOT NULL
);

CREATE TABLE Bestellung (
    BestellNr INTEGER PRIMARY KEY,
    Datum     TEXT NOT NULL,
    KundenNr  INTEGER,
    FOREIGN KEY (KundenNr) REFERENCES Kunde (KundenNr)
);

INSERT INTO Kunde (KundenNr, Name, Ort) VALUES
    (1, 'Berger, Anna', 'Dresden'),
    (2, 'Kaufmann, Ben', 'Radebeul'),
    (3, 'Nowak, Clara', 'Dresden'),
    (4, 'Vogt, David', 'Meißen'),
    (5, 'Hein, Emil', 'Dresden'),
    (6, 'Sommer, Ida', 'Pirna'),
    (7, 'Roth, Jonas', 'Radebeul'),
    (8, 'Lang, Katja', 'Dresden');

INSERT INTO Produkt (ProduktNr, Bezeichnung, Preis) VALUES
    (101, 'Tastatur', 29.99),
    (102, 'Funkmaus', 19.5),
    (103, 'Monitor 24 Zoll', 149.0),
    (104, 'USB-Stick 64 GB', 9.99),
    (105, 'Headset', 59.9),
    (106, 'Webcam', 44.5),
    (107, 'Notebooktasche', 24.9),
    (108, 'Dockingstation', 119.0),
    (109, 'Mauspad', 6.5),
    (110, 'Kabeltrommel', 34.0);

INSERT INTO Bestellung (BestellNr, Datum, KundenNr) VALUES
    (5001, '2026-03-02', 1),
    (5002, '2026-03-02', 3),
    (5003, '2026-03-05', 2),
    (5004, '2026-03-09', 1),
    (5005, '2026-03-11', 5),
    (5006, '2026-03-12', 4),
    (5007, '2026-03-16', 3),
    (5008, '2026-03-18', 6),
    (5009, '2026-03-23', 7),
    (5010, '2026-03-24', 1),
    (5011, '2026-04-02', 5),
    (5012, '2026-04-07', 2);

-- Tabellenstruktur
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS schueler;
DROP TABLE IF EXISTS klasse;

CREATE TABLE klasse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE schueler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    klasse_id INTEGER,
    FOREIGN KEY (klasse_id) REFERENCES klasse(id)
);

CREATE TABLE note (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schueler_id INTEGER,
    wert REAL,
    FOREIGN KEY (schueler_id) REFERENCES schueler(id)
);

-- Klassen
INSERT INTO klasse (name) VALUES 
('10A'), ('10B'), ('9C');

-- Schüler*innen
INSERT INTO schueler (name, klasse_id) VALUES 
('Anna Müller', 1),
('Lukas Schulz', 1),
('Felix Test', 1),
('Marie Becker', 2),
('Tom Schneider', 2),
('Sarah Müller', 3),
('Leon Koch', 3),
('Anna Müller', 3);

-- Noten
INSERT INTO note (schueler_id, wert) VALUES 
(1, 1.7),
(1, 2.3),
(2, 2.0),
(3, 3.0),
(4, 1.3),
(4, 1.0),
(5, 3.7),
(6, 2.7),
(7, 2.0),
(8, 1.7);

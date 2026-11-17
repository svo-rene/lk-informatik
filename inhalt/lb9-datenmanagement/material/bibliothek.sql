-- Tabelle für Autoren
CREATE TABLE IF NOT EXISTS Autoren (
    AutorID INTEGER PRIMARY KEY AUTOINCREMENT,
    Vorname TEXT,
    Nachname TEXT,
    Geburtsjahr INTEGER
);

-- Tabelle für Bücher
CREATE TABLE IF NOT EXISTS Buecher (
    BuchID INTEGER PRIMARY KEY AUTOINCREMENT,
    Titel TEXT,
    AutorID INTEGER,
    Erscheinungsjahr INTEGER,
    ISBN TEXT,
    FOREIGN KEY (AutorID) REFERENCES Autoren(AutorID)
);

-- Tabelle für Nutzer
CREATE TABLE IF NOT EXISTS Nutzer (
    NutzerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Vorname TEXT,
    Nachname TEXT,
    Email TEXT,
    Registrierungsdatum TEXT
);

-- Tabelle für Ausleihen
CREATE TABLE IF NOT EXISTS Ausleihen (
    AusleiheID INTEGER PRIMARY KEY AUTOINCREMENT,
    BuchID INTEGER,
    NutzerID INTEGER,
    Ausleihdatum TEXT,
    Rueckgabedatum TEXT,
    FOREIGN KEY (BuchID) REFERENCES Buecher(BuchID),
    FOREIGN KEY (NutzerID) REFERENCES Nutzer(NutzerID)
);

-- Einfügen von Beispieldaten für Autoren
INSERT INTO Autoren (Vorname, Nachname, Geburtsjahr) VALUES
('Johann Wolfgang', 'von Goethe', 1749),
('Friedrich', 'Schiller', 1759),
('Thomas', 'Mann', 1875),
('Hermann', 'Hesse', 1877),
('Bertolt', 'Brecht', 1898),
('Franz', 'Kafka', 1883),
('Heinrich', 'Böll', 1917),
('Günter', 'Grass', 1927),
('Max', 'Frisch', 1911),
('Friedrich', 'Dürrenmatt', 1921),
('Stefan', 'Zweig', 1881),
('Erich', 'Kästner', 1899),
('Theodor', 'Fontane', 1819),
('Lion', 'Feuchtwanger', 1884),
('Elfriede', 'Jelinek', 1946);

-- Einfügen von Beispieldaten für Bücher
INSERT INTO Buecher (Titel, AutorID, Erscheinungsjahr, ISBN) VALUES
('Faust', 1, 1808, '9783150000012'),
('Die Räuber', 2, 1781, '9783150000029'),
('Der Zauberberg', 3, 1924, '9783150000036'),
('Siddharta', 4, 1922, '9783150000043'),
('Mutter Courage und ihre Kinder', 5, 1939, '9783150000050'),
('Die Verwandlung', 6, 1915, '9783150000067'),
('Ansichten eines Clowns', 7, 1963, '9783150000074'),
('Die Blechtrommel', 8, 1959, '9783150000081'),
('Homo Faber', 9, 1957, '9783150000098'),
('Der Besuch der alten Dame', 10, 1956, '9783150000104'),
('Die Welt von Gestern', 11, 1942, '9783150000111'),
('Emil und die Detektive', 12, 1929, '9783150000128'),
('Effi Briest', 13, 1895, '9783150000135'),
('Jud Süß', 14, 1925, '9783150000142'),
('Die Klavierspielerin', 15, 1983, '9783150000159'),
('Wilhelm Meisters Lehrjahre', 1, 1795, '9783150000166'),
('Kabale und Liebe', 2, 1784, '9783150000173'),
('Buddenbrooks', 3, 1901, '9783150000180'),
('Der Steppenwolf', 4, 1927, '9783150000197'),
('Leben des Galilei', 5, 1939, '9783150000203');

-- Einfügen von Beispieldaten für Nutzer
INSERT INTO Nutzer (Vorname, Nachname, Email, Registrierungsdatum) VALUES
('Max', 'Mustermann', 'max.mustermann@example.com', '2024-01-15'),
('Anna', 'Schmidt', 'anna.schmidt@example.com', '2024-02-20'),
('Lena', 'Weber', 'lena.weber@example.com', '2024-03-10'),
('Tim', 'Müller', 'tim.mueller@example.com', '2024-04-05'),
('Sara', 'Fischer', 'sara.fischer@example.com', '2024-05-01'),
('Laura', 'Becker', 'laura.becker@example.com', '2024-05-15'),
('Felix', 'Klein', 'felix.klein@example.com', '2024-06-01'),
('Sophie', 'Wagner', 'sophie.wagner@example.com', '2024-06-15'),
('Lukas', 'Hoffmann', 'lukas.hoffmann@example.com', '2024-07-01'),
('Emma', 'Schneider', 'emma.schneider@example.com', '2024-07-15'),
('Noah', 'Meyer', 'noah.meyer@example.com', '2024-08-01'),
('Mia', 'Wolf', 'mia.wolf@example.com', '2024-08-15'),
('Leon', 'Bauer', 'leon.bauer@example.com', '2024-09-01'),
('Hannah', 'Koch', 'hannah.koch@example.com', '2024-09-15'),
('Paul', 'Richter', 'paul.richter@example.com', '2024-10-01');

-- Einfügen von Beispieldaten für Ausleihen
INSERT INTO Ausleihen (BuchID, NutzerID, Ausleihdatum, Rueckgabedatum) VALUES
(1, 1, '2024-09-01', '2024-09-15'),
(2, 2, '2024-09-05', '2024-09-19'),
(3, 3, '2024-09-10', '2024-09-24'),
(4, 4, '2024-09-15', '2024-09-29'),
(5, 5, '2024-09-20', '2024-10-04'),
(6, 6, '2024-09-25', '2024-10-09'),
(7, 7, '2024-09-30', '2024-10-14'),
(8, 8, '2024-10-05', '2024-10-19'),
(9, 9, '2024-10-10', '2024-10-24'),
(10, 10, '2024-10-15', '2024-10-29'),
(11, 11, '2024-10-20', '2024-11-03'),
(12, 12, '2024-10-25', '2024-11-08'),
(13, 13, '2024-10-30', '2024-11-13'),
(14, 14, '2024-11-04', '2024-11-18'),
(15, 15, '2024-11-09', '2024-11-23'),
(16, 1, '2024-11-14', '2024-11-28'),
(17, 2, '2024-11-19', '2024-12-03'),
(18, 3, '2024-11-24', '2024-12-08'),
(19, 4, '2024-11-29', '2024-12-13'),
(20, 5, '2024-12-04', '2024-12-18');
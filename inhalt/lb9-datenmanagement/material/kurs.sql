-- Erstellen der Tabelle Schueler
CREATE TABLE Schueler (
    s_id INT PRIMARY KEY,
    name VARCHAR(50),
    vorname VARCHAR(50)
);

-- Einfügen von Beispieldaten in die Tabelle Schueler
INSERT INTO Schueler (s_id, name, vorname) VALUES
(1, 'Müller', 'Lisa'),
(2, 'Schmidt', 'Max'),
(3, 'Fischer', 'Anna'),
(4, 'Weber', 'Tim'),
(5, 'Meyer', 'Sophie');

-- Erstellen der Tabelle Kurs
CREATE TABLE Kurs (
    k_id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- Einfügen von Beispieldaten in die Tabelle Kurs
INSERT INTO Kurs (k_id, name) VALUES
(1, 'Mathematik'),
(2, 'Deutsch'),
(3, 'Englisch'),
(4, 'Biologie'),
(5, 'Geschichte');

-- Erstellen der Tabelle Kursnote
CREATE TABLE Kursnote (
    k_id INT,
    s_id INT,
    note DECIMAL(2,1),
    PRIMARY KEY (k_id, s_id),
    FOREIGN KEY (k_id) REFERENCES Kurs(k_id),
    FOREIGN KEY (s_id) REFERENCES Schueler(s_id)
);

-- Einfügen von Beispieldaten in die Tabelle Kursnote
INSERT INTO Kursnote (k_id, s_id, note) VALUES
(1, 1, 2.3),
(1, 2, 1.7),
(2, 1, 1.3),
(2, 3, 2.0),
(3, 2, 1.0),
(3, 4, 2.7),
(4, 3, 1.7),
(4, 5, 2.3),
(5, 4, 1.3),
(5, 5, 2.0);
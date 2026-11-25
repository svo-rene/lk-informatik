-- Erstellen der Tabelle Verkäufe
CREATE TABLE Verkäufe (
    VerkaufID INTEGER PRIMARY KEY AUTOINCREMENT,
    Produkt TEXT NOT NULL,
    Menge INTEGER NOT NULL,
    Preis DECIMAL(10, 2) NOT NULL,
    Datum DATE NOT NULL
);

-- Einfügen von Beispieldaten
INSERT INTO Verkäufe (Produkt, Menge, Preis, Datum) VALUES
('Laptop', 2, 999.99, '2023-01-15'),
('Smartphone', 5, 599.99, '2023-01-16'),
('Tablet', 3, 399.99, '2023-01-17'),
('Kopfhörer', 10, 79.99, '2023-01-18'),
('Maus', 15, 29.99, '2023-01-19'),
('Monitor', 4, 249.99, '2023-01-20'),
('Tastatur', 8, 59.99, '2023-01-21'),
('Drucker', 2, 179.99, '2023-01-22'),
('Festplatte', 6, 89.99, '2023-01-23'),
('Grafikkarte', 3, 399.99, '2023-01-24'),
('Laptop', 3, 1099.99, '2023-01-25'),
('Smartphone', 7, 649.99, '2023-01-26'),
('Tablet', 4, 449.99, '2023-01-27'),
('Kopfhörer', 12, 89.99, '2023-01-28'),
('Maus', 20, 34.99, '2023-01-29'),
('Monitor', 5, 279.99, '2023-01-30'),
('Tastatur', 10, 69.99, '2023-01-31'),
('Drucker', 3, 199.99, '2023-02-01'),
('Festplatte', 8, 99.99, '2023-02-02'),
('Grafikkarte', 2, 449.99, '2023-02-03');

-- Überprüfen der eingefügten Daten
SELECT * FROM Verkäufe;

-- Zählen der Gesamtanzahl der Verkäufe
SELECT COUNT(*) as AnzahlVerkäufe FROM Verkäufe;

-- Berechnen des Gesamtumsatzes
SELECT SUM(Menge * Preis) as Gesamtumsatz FROM Verkäufe;

-- Erstellen der Tabelle für Attraktionen
CREATE TABLE attractions (
    attraction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    attraction_name TEXT NOT NULL,
    description TEXT,
    suitable_for_children BOOLEAN NOT NULL,
    difficulty_level TEXT,
    annual_visitors INTEGER,
    ticket_price REAL
);

-- Beispiel-Datensätze für Attraktionen
INSERT INTO attractions (attraction_name, description, suitable_for_children, difficulty_level, annual_visitors, ticket_price) VALUES
('Achterbahn', 'Spannende Hochgeschwindigkeits-Achterbahn', 1, 'Mittel', 1200, 15.00),
('Riesenrad', 'Genieße eine ruhige Fahrt und die Aussicht', 1, 'Leicht', 500, 8.50),
('Geisterbahn', 'Gruselspaß für die ganze Familie', 1, 'Mittel', 700, 12.00),
('Wasserpark', 'Erfrischung an heißen Tagen mit vielen Rutschen', 1, 'Leicht', 2000, 20.00),
('Freefall Tower', 'Atemberaubender Fall aus großer Höhe', 0, 'Schwer', 1500, 18.00);

-- Erstellen der Tabelle für Shows
CREATE TABLE shows (
    show_id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_name TEXT NOT NULL,
    show_time DATETIME NOT NULL,
    location TEXT NOT NULL,
    budget REAL,
    daily_visitors INTEGER
);

-- Beispiel-Datensätze für Shows
INSERT INTO shows (show_name, show_time, location, budget, daily_visitors) VALUES
('Feuerwerk Show', '2024-08-12 21:00', 'Main Stage', 500.00, 300),
('Zaubershow', '2024-08-13 15:00', 'Theaterzelt', 300.00, 150),
('Akrobatik-Show', '2024-08-14 16:30', 'Hauptbühne', 400.00, 200),
('Parade', '2024-08-15 14:00', 'Parkstraße', 250.00, 400),
('Comedy Show', '2024-08-16 17:30', 'Komödienzelt', 200.00, 100);

-- Erstellen der Tabelle für Besucher
CREATE TABLE visitors (
    visitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    year_of_birth INTEGER
);

-- Beispiel-Datensätze für Besucher
INSERT INTO visitors (name, age, year_of_birth) VALUES
('Lena Schmidt', 25, 1998),
('Tom Huber', 30, 1993),
('Julia Becker', 17, 2006),
('Peter Weber', 14, 2009),
('Anna Meier', 22, 2001);

-- Erstellen der Tabelle für Tickets
CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_id INTEGER NOT NULL,
    ticket_type TEXT NOT NULL,
    price REAL NOT NULL,
    purchase_date DATE,
    FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id)
);

-- Beispiel-Datensätze für Tickets
INSERT INTO tickets (visitor_id, ticket_type, price, purchase_date) VALUES
(1, 'VIP', 50.00, '2024-08-10'),
(2, 'Standard', 25.00, '2024-08-11'),
(3, 'VIP', 50.00, '2024-08-12'),
(4, 'Standard', 25.00, '2024-08-13'),
(5, 'Standard', 25.00, '2024-08-14');

-- Erstellen der Tabelle für Buchungen
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_id INTEGER NOT NULL,
    attraction_id INTEGER,
    show_id INTEGER,
    booking_date DATE,
    booking_type TEXT CHECK(booking_type IN ('attraction', 'show')),
    FOREIGN KEY (visitor_id) REFERENCES visitors(visitor_id),
    FOREIGN KEY (attraction_id) REFERENCES attractions(attraction_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

-- Beispiel-Datensätze für Buchungen
INSERT INTO bookings (visitor_id, attraction_id, booking_date, booking_type) VALUES
(1, 1, '2024-08-10', 'attraction'),
(2, 3, '2024-08-11', 'attraction'),
(3, 2, '2024-08-12', 'attraction'),
(4, 5, '2024-08-13', 'attraction'),
(5, 4, '2024-08-14', 'attraction');

INSERT INTO bookings (visitor_id, show_id, booking_date, booking_type) VALUES
(1, 1, '2024-08-10', 'show'),
(2, 2, '2024-08-11', 'show'),
(3, 3, '2024-08-12', 'show'),
(4, 4, '2024-08-13', 'show'),
(5, 5, '2024-08-14', 'show');
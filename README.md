# Viastore Demo – Dokumentation

## Übersicht
Dieses Projekt ist eine Demo-Anwendung für Lagerverwaltung, Artikelverwaltung und Bestellmanagement mit Touch-optimierter Wareneingangsbuchung. Es basiert auf Django und Bootstrap.

## Features
- Dashboard mit Statistiken und Diagramm
- Lager, Artikel und Bestellungen anlegen und verwalten
- Bestandskorrektur und Bestandsauskunft
- Wareneingang (Standard und Touch-Version)
- Sidebar-Navigation mit Icons
- Benutzer-Login und Logout, Zugriffsschutz für alle Seiten
- Touch-Anwendung unter /touch/ (ohne Sidebar)
- Admin-Bereich für Superuser

## Installation
1. **Voraussetzungen:** Python 3.12, Django 5.x
2. **Projekt entpacken:**
	```
	unzip viastore_download.zip
	cd Test
	```
3. **Abhängigkeiten installieren:**
	```
	pip install django
	```
4. **Migrationen ausführen:**
	```
	python manage.py migrate
	```
5. **Superuser anlegen:**
	```
	python manage.py createsuperuser
	```
	(Standard: Benutzername `Admin`, Passwort `Tel.22879044`)
6. **Server starten:**
	```
	python manage.py runserver
	```

## Nutzung
- **Dashboard:** Übersicht, Buttons für alle Funktionen
- **Sidebar:** Navigation zu Lager, Artikel, Bestellungen, Wareneingang, Bestandskorrektur, Bestandsauskunft
- **Touch-Version:** `/touch/` – optimiert für Tablets, nur Wareneingang
- **Login:** `/login/` – alle Seiten sind geschützt
- **Admin:** `/admin/` – Django Admin für alle Modelle

## Datenmodelle
### Warehouse
- name: Name des Lagers
- location: Standort

### Item
- name: Artikelname
- sku: Artikelnummer
- quantity: Bestand
- warehouse: Lagerzuordnung

### Order
- order_number: Bestellnummer
- item: Artikel
- quantity: Menge
- order_date: Datum

## Wichtige Views & URLs
- `/` – Dashboard
- `/lager-anlegen/` – Lager anlegen
- `/artikel-anlegen/` – Artikel anlegen
- `/bestellung-anlegen/` – Bestellung anlegen
- `/wareneingang/` – Wareneingang buchen
- `/wareneingang-touch/` – Wareneingang Touch (als Modal)
- `/touch/` – Separate Touch-Anwendung
- `/bestandskorrektur/` – Bestandskorrektur
- `/bestandsauskunft/` – Bestandsauskunft
- `/bestellungen/` – Bestellungen anzeigen
- `/login/` – Login
- `/logout/` – Logout
- `/admin/` – Django Admin

## Sicherheit
- Alle Seiten sind nur nach Login erreichbar
- Login/Logout über eigene Views
- Superuser kann im Admin alles verwalten

## Erweiterung
Das Projekt kann beliebig erweitert werden, z.B. um weitere Funktionen, API-Endpunkte oder ein responsives Design.

## Kontakt
Fragen und Support: [Dein Name/Team]
# Viastore Demo – Dokumentation

## Übersicht
Dieses Projekt ist eine Demo-Anwendung für Lagerverwaltung, Artikelverwaltung und Bestellmanagement mit JWT-basierter Token-Authentifizierung. Es basiert auf Django und Django REST Framework.

## Features
- JWT-basierte Token-Authentifizierung (kein Cookie-Login)
- RESTful API-Endpunkte für alle Funktionen
- Dashboard mit Statistiken
- Lager, Artikel und Bestellungen über API verwalten
- Bestandskorrektur und Bestandsauskunft über API
- Wareneingang (Standard und Touch-Version) über API
- Excel-Import über API
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

## Verwendung der API
- **Authentifizierung:** JWT-Token über `/api/token-login/` abrufen
- **Dashboard:** Statistiken über `/api/dashboard/` abrufen
- **Lager:** Über `/api/lager/` verwalten
- **Artikel:** Über `/api/artikel/` verwalten
- **Bestellungen:** Über `/api/bestellungen/` verwalten
- **Wareneingang:** Über `/api/wareneingang/` buchen
- **Admin:** `/admin/` – Django Admin für Superuser

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

## API-Endpunkte

### Authentifizierung
- `POST /api/token-login/` – JWT Token Login
  - Body: `{"username": "...", "password": "..."}`
  - Response: `{"access": "...", "refresh": "..."}`

### Dashboard
- `GET /api/dashboard/` – Dashboard-Statistiken

### Lager (Warehouse)
- `GET /api/lager/` – Alle Lager auflisten
- `POST /api/lager/` – Neues Lager anlegen

### Artikel (Items)
- `GET /api/artikel/` – Alle Artikel auflisten
- `POST /api/artikel/` – Neuen Artikel anlegen
- `GET /api/artikel/<id>/` – Artikel-Details abrufen
- `PUT /api/artikel/<id>/` – Artikel aktualisieren
- `PATCH /api/artikel/<id>/` – Artikel teilweise aktualisieren
- `DELETE /api/artikel/<id>/` – Artikel löschen
- `GET /api/item-bestand/<id>/` – Artikelbestand abrufen
- `GET /api/item-info/<sku>/` – Artikel-Info nach SKU

### Bestellungen (Orders)
- `GET /api/bestellungen/` – Alle Bestellungen auflisten
- `POST /api/bestellungen/` – Neue Bestellung anlegen

### Wareneingang (Goods Receipt)
- `POST /api/wareneingang/` – Wareneingang buchen
- `POST /api/wareneingang-touch/` – Touch-Wareneingang

### Bestandsverwaltung (Stock Management)
- `GET /api/bestandsauskunft/` – Bestandsauskunft für alle Artikel
- `POST /api/bestandskorrektur/` – Bestandskorrektur durchführen

### Import
- `POST /api/import-excel/` – Excel-Import

### Externe Daten
- `GET /api/google-item-info/<sku>/` – Artikel-Info von Google

## Sicherheit
- Alle API-Endpunkte sind JWT-geschützt (außer `/api/token-login/` und `/api/google-item-info/`)
- Jede Anfrage muss den Header `Authorization: Bearer <access_token>` enthalten
- Tokens sind 1 Stunde gültig (Access Token), Refresh Tokens 1 Tag

## Verwendung

### 1. Token abrufen
```bash
curl -X POST http://localhost:8000/api/token-login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### 2. API-Anfrage mit Token
```bash
curl -X GET http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Erweiterung
Das Projekt kann beliebig erweitert werden, z.B. um weitere Funktionen, API-Endpunkte oder ein responsives Design.

## Kontakt
Fragen und Support: [Dein Name/Team]
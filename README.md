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
2. **Repository klonen:**
	```bash
	git clone https://github.com/sn4200/Test.git
	cd Test
	```
3. **Abhängigkeiten installieren:**
	```bash
	pip install -r requirements.txt
	```
4. **Migrationen ausführen:**
	```bash
	python manage.py migrate
	```
5. **Superuser erstellen:**
	```bash
	python manage.py createsuperuser
	```
6. **Server starten:**
	```bash
	python manage.py runserver
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

## Beispiele

### Vollständiger Workflow

#### 1. Login und Token erhalten
```bash
curl -X POST http://localhost:8000/api/token-login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 2. Lager erstellen
```bash
curl -X POST http://localhost:8000/api/lager/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hauptlager", "location": "Berlin"}'
```

#### 3. Artikel erstellen
```bash
curl -X POST http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Schrauben M8", "sku": "SCR-M8-001", "quantity": 100, "warehouse": 1}'
```

#### 4. Wareneingang buchen
```bash
curl -X POST http://localhost:8000/api/wareneingang/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"item": 1, "quantity": 50}'
```

#### 5. Artikel aktualisieren
```bash
curl -X PATCH http://localhost:8000/api/artikel/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Schrauben M8 verzinkt"}'
```

#### 6. Bestandskorrektur durchführen
```bash
curl -X POST http://localhost:8000/api/bestandskorrektur/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"item": 1, "new_quantity": 200}'
```

#### 7. Alle Artikel abrufen
```bash
curl -X GET http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer <access_token>"
```

#### 8. Bestellung erstellen
```bash
curl -X POST http://localhost:8000/api/bestellungen/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"order_number": "ORD-001", "item": 1, "quantity": 25}'
```

## Erweiterung
Das Projekt kann beliebig erweitert werden, z.B. um weitere Funktionen oder API-Endpunkte.

## Kontakt
Fragen und Support: [Dein Name/Team]
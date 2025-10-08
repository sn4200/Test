# API Overview

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Viastore API                            │
│                  JWT Token Authentication                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐        ┌─────▼──────┐      ┌────▼─────┐
    │ Auth   │        │  Business  │      │ External │
    │ Layer  │        │   Logic    │      │   APIs   │
    └───┬────┘        └─────┬──────┘      └────┬─────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │    Database    │
                    │   (SQLite)     │
                    └────────────────┘
```

## API Endpoints Summary

### Authentication (Public)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/token-login/` | Obtain JWT access and refresh tokens | ❌ |

### Dashboard (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/dashboard/` | Get warehouse, item, and order counts | ✅ |

### Warehouse Management (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/lager/` | List all warehouses | ✅ |
| POST | `/api/lager/` | Create new warehouse | ✅ |

### Item Management (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/artikel/` | List all items | ✅ |
| POST | `/api/artikel/` | Create new item | ✅ |
| GET | `/api/artikel/<id>/` | Get item details | ✅ |
| PUT | `/api/artikel/<id>/` | Update item (full) | ✅ |
| PATCH | `/api/artikel/<id>/` | Update item (partial) | ✅ |
| DELETE | `/api/artikel/<id>/` | Delete item | ✅ |
| GET | `/api/item-bestand/<id>/` | Get item stock | ✅ |
| GET | `/api/item-info/<sku>/` | Get item by SKU | ✅ |

### Order Management (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/bestellungen/` | List all orders | ✅ |
| POST | `/api/bestellungen/` | Create new order | ✅ |

### Goods Receipt (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/wareneingang/` | Book goods receipt | ✅ |
| POST | `/api/wareneingang-touch/` | Book via touch interface | ✅ |

### Stock Management (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/bestandsauskunft/` | Get stock info for all items | ✅ |
| POST | `/api/bestandskorrektur/` | Correct item stock | ✅ |

### Data Import (Protected)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/import-excel/` | Import items from Excel | ✅ |

### External Data (Public)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/google-item-info/<sku>/` | Fetch item info from Google | ❌ |

## Data Models

### Warehouse
```json
{
  "id": 1,
  "name": "Hauptlager",
  "location": "Berlin"
}
```

### Item
```json
{
  "id": 1,
  "name": "Schrauben M8",
  "sku": "SCR-M8-001",
  "quantity": 100,
  "warehouse": 1,
  "warehouse_name": "Hauptlager"
}
```

### Item Detail (with warehouse info)
```json
{
  "id": 1,
  "name": "Schrauben M8",
  "sku": "SCR-M8-001",
  "quantity": 100,
  "warehouse": 1,
  "warehouse_name": "Hauptlager",
  "warehouse_location": "Berlin"
}
```

### Order
```json
{
  "id": 1,
  "order_number": "ORD-2025-001",
  "item": 1,
  "item_name": "Schrauben M8",
  "item_sku": "SCR-M8-001",
  "quantity": 50,
  "order_date": "2025-10-08T12:00:00Z"
}
```

## Authentication Flow

```
┌──────────┐                                      ┌──────────┐
│  Client  │                                      │  Server  │
└────┬─────┘                                      └────┬─────┘
     │                                                 │
     │  POST /api/token-login/                        │
     │  {username, password}                          │
     ├────────────────────────────────────────────────>│
     │                                                 │
     │  {access, refresh}                             │
     │<────────────────────────────────────────────────┤
     │                                                 │
     │  GET /api/artikel/                             │
     │  Authorization: Bearer <access>                │
     ├────────────────────────────────────────────────>│
     │                                                 │
     │  Validate Token                                │
     │                                      ┌──────────┤
     │                                      │  JWT     │
     │                                      │  Valid?  │
     │                                      └──────────┤
     │                                                 │
     │  [Items List]                                  │
     │<────────────────────────────────────────────────┤
     │                                                 │
```

## Request/Response Examples

### Login
**Request:**
```http
POST /api/token-login/ HTTP/1.1
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Create Item
**Request:**
```http
POST /api/artikel/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "Schrauben M8",
  "sku": "SCR-M8-001",
  "quantity": 100,
  "warehouse": 1
}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "name": "Schrauben M8",
  "sku": "SCR-M8-001",
  "quantity": 100,
  "warehouse": 1,
  "warehouse_name": "Hauptlager"
}
```

### Book Goods Receipt
**Request:**
```http
POST /api/wareneingang/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "item": 1,
  "quantity": 25
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Wareneingang für Schrauben M8 (SCR-M8-001) erfolgreich gebucht!",
  "item": {
    "id": 1,
    "name": "Schrauben M8",
    "sku": "SCR-M8-001",
    "quantity": 125,
    "warehouse": 1,
    "warehouse_name": "Hauptlager"
  }
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 400 Bad Request
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

## Security Features

- ✅ JWT-based authentication (no cookies)
- ✅ Token expiration (1 hour for access, 1 day for refresh)
- ✅ Permission-based access control
- ✅ CSRF protection via JWT
- ✅ All endpoints protected by default
- ✅ Secure password hashing (Django default)

## Performance Considerations

- Database queries optimized with `select_related()` and `prefetch_related()`
- Pagination can be added for large datasets
- Token-based auth reduces server-side session storage
- RESTful design allows for efficient caching

## Future Enhancements

- [ ] Add pagination for list endpoints
- [ ] Implement filtering and search
- [ ] Add sorting capabilities
- [ ] Rate limiting
- [ ] API versioning
- [ ] WebSocket support for real-time updates
- [ ] File upload for item images
- [ ] Bulk operations
- [ ] Advanced reporting endpoints
- [ ] Integration with external ERP systems

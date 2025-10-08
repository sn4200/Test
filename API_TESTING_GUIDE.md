# API Testing Guide

This guide provides comprehensive instructions for testing the Viastore API endpoints.

## Prerequisites

1. Django server running on `http://localhost:8000`
2. Valid user credentials (username and password)
3. `curl` or any HTTP client (Postman, Insomnia, etc.)

## Authentication

All API endpoints (except `/api/token-login/` and `/api/google-item-info/`) require JWT authentication.

### Step 1: Obtain JWT Token

```bash
curl -X POST http://localhost:8000/api/token-login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Save the `access` token for use in subsequent requests.

### Step 2: Use Token in Requests

Include the token in the `Authorization` header:

```bash
Authorization: Bearer <your_access_token>
```

## API Endpoints Testing

### 1. Dashboard

**Get dashboard statistics:**
```bash
curl -X GET http://localhost:8000/api/dashboard/ \
  -H "Authorization: Bearer <token>"
```

**Expected Response:**
```json
{
  "warehouse_count": 4,
  "item_count": 12,
  "order_count": 5
}
```

### 2. Warehouse Management

**List all warehouses:**
```bash
curl -X GET http://localhost:8000/api/lager/ \
  -H "Authorization: Bearer <token>"
```

**Create a new warehouse:**
```bash
curl -X POST http://localhost:8000/api/lager/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Hauptlager", "location": "Berlin"}'
```

### 3. Item Management

**List all items:**
```bash
curl -X GET http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer <token>"
```

**Create a new item:**
```bash
curl -X POST http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Schrauben M8",
    "sku": "SCR-M8-001",
    "quantity": 100,
    "warehouse": 1
  }'
```

**Get item details:**
```bash
curl -X GET http://localhost:8000/api/artikel/1/ \
  -H "Authorization: Bearer <token>"
```

**Update an item (partial):**
```bash
curl -X PATCH http://localhost:8000/api/artikel/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Schrauben M8 verzinkt"}'
```

**Update an item (full):**
```bash
curl -X PUT http://localhost:8000/api/artikel/1/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Schrauben M8 verzinkt",
    "sku": "SCR-M8-001",
    "quantity": 150,
    "warehouse": 1
  }'
```

**Delete an item:**
```bash
curl -X DELETE http://localhost:8000/api/artikel/1/ \
  -H "Authorization: Bearer <token>"
```

### 4. Order Management

**List all orders:**
```bash
curl -X GET http://localhost:8000/api/bestellungen/ \
  -H "Authorization: Bearer <token>"
```

**Create a new order:**
```bash
curl -X POST http://localhost:8000/api/bestellungen/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "order_number": "ORD-2025-001",
    "item": 1,
    "quantity": 50
  }'
```

### 5. Goods Receipt

**Book goods receipt:**
```bash
curl -X POST http://localhost:8000/api/wareneingang/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item": 1,
    "quantity": 25
  }'
```

**Expected Response:**
```json
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

### 6. Touch Interface Goods Receipt

**Book goods receipt via touch interface:**
```bash
curl -X POST http://localhost:8000/api/wareneingang-touch/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item_name": 12345678,
    "quantity": 10
  }'
```

Note: If the item doesn't exist, it will be created automatically with the SKU fetched from external sources.

### 7. Stock Management

**Get stock information for all items:**
```bash
curl -X GET http://localhost:8000/api/bestandsauskunft/ \
  -H "Authorization: Bearer <token>"
```

**Correct item stock:**
```bash
curl -X POST http://localhost:8000/api/bestandskorrektur/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "item": 1,
    "new_quantity": 200
  }'
```

**Expected Response:**
```json
{
  "message": "Bestand erfolgreich korrigiert!",
  "item": {
    "id": 1,
    "name": "Schrauben M8",
    "sku": "SCR-M8-001",
    "quantity": 200,
    "warehouse": 1,
    "warehouse_name": "Hauptlager"
  },
  "old_quantity": 125,
  "new_quantity": 200
}
```

### 8. Item Information

**Get item by SKU:**
```bash
curl -X GET http://localhost:8000/api/item-info/SCR-M8-001/ \
  -H "Authorization: Bearer <token>"
```

**Get item stock by ID:**
```bash
curl -X GET http://localhost:8000/api/item-bestand/1/ \
  -H "Authorization: Bearer <token>"
```

### 9. Excel Import

**Import items from Excel file:**
```bash
curl -X POST http://localhost:8000/api/import-excel/ \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/your/file.xlsx"
```

Excel file format:
- Column A: Item Name
- Column B: SKU
- Column C: Quantity
- Column D: Warehouse Name

### 10. External Data

**Get item information from Google (no authentication required):**
```bash
curl -X GET http://localhost:8000/api/google-item-info/12345678/
```

## Error Handling

### Authentication Errors

**Missing token:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Invalid token:**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### Validation Errors

**Invalid data:**
```json
{
  "field_name": [
    "This field is required."
  ]
}
```

### Not Found Errors

**Item not found:**
```json
{
  "detail": "Not found."
}
```

## Testing with Python

You can also use Python's `requests` library:

```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/api/token-login/',
    json={'username': 'your_username', 'password': 'your_password'}
)
token = response.json()['access']

# Use the token
headers = {'Authorization': f'Bearer {token}'}

# Get dashboard
dashboard = requests.get('http://localhost:8000/api/dashboard/', headers=headers)
print(dashboard.json())

# Create warehouse
new_warehouse = requests.post(
    'http://localhost:8000/api/lager/',
    headers=headers,
    json={'name': 'Hauptlager', 'location': 'Berlin'}
)
print(new_warehouse.json())
```

## Token Refresh

Access tokens expire after 1 hour. Use the refresh token to obtain a new access token:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<your_refresh_token>"}'
```

## Best Practices

1. **Always use HTTPS in production** to protect tokens from interception
2. **Store tokens securely** (e.g., in environment variables, secure storage)
3. **Handle token expiration** by implementing refresh logic
4. **Validate responses** and handle errors appropriately
5. **Use appropriate HTTP methods** (GET for retrieval, POST for creation, PUT/PATCH for updates, DELETE for deletion)

## Common Issues

1. **CSRF Token Error**: API endpoints use JWT authentication, so CSRF tokens are not needed
2. **CORS Issues**: If accessing from a different domain, ensure CORS is properly configured
3. **Token Expiration**: Implement token refresh logic to handle expired tokens
4. **Rate Limiting**: Consider implementing rate limiting in production

## Support

For issues or questions, refer to the main README.md or contact the development team.

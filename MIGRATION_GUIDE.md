# Migration Guide: Cookie-Based to JWT Token Authentication

This guide explains the changes from the old cookie-based authentication system to the new JWT token-based API.

## Overview of Changes

### Before (Cookie-Based)
- Traditional Django views with `@login_required` decorators
- Session cookies for authentication
- Server-side session storage
- HTML template rendering
- Form-based interactions

### After (JWT Token-Based)
- RESTful API with JWT authentication
- Stateless authentication (no server-side sessions)
- JSON responses
- API-based interactions
- Token-based authorization

## Key Differences

### Authentication Method

#### Old System (Cookies)
```python
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # ... logic ...
    return render(request, "dashboard.html", context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Creates session cookie
            return redirect("dashboard")
    # ...
```

#### New System (JWT)
```python
# api_views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class TokenLoginView(TokenObtainPairView):
    """Returns JWT access and refresh tokens"""
    permission_classes = [AllowAny]

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # ... logic ...
        return Response(data)  # Returns JSON
```

### URL Configuration

#### Old URLs
```python
# urls.py
urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("artikel/", item_list, name="item_list"),
    path("artikel-anlegen/", add_item, name="add_item"),
    # ... more HTML-based routes
]
```

#### New URLs
```python
# urls.py
urlpatterns = [
    # Authentication
    path("api/token-login/", TokenLoginView.as_view(), name="token_login"),
    
    # API endpoints
    path("api/dashboard/", DashboardAPIView.as_view(), name="dashboard"),
    path("api/artikel/", ItemListCreateAPIView.as_view(), name="item_list_create"),
    path("api/artikel/<int:pk>/", ItemDetailAPIView.as_view(), name="item_detail"),
    # ... more API routes
]
```

### Client Usage

#### Old System (Browser/Form)
```html
<!-- login.html -->
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>

<!-- After login, session cookie automatically sent with each request -->
```

#### New System (API Client)
```bash
# 1. Login to get token
curl -X POST http://localhost:8000/api/token-login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Response:
# {"access": "eyJhbG...", "refresh": "eyJhbG..."}

# 2. Use token in subsequent requests
curl -X GET http://localhost:8000/api/artikel/ \
  -H "Authorization: Bearer eyJhbG..."
```

## Endpoint Mapping

### Dashboard
| Old | New | Method |
|-----|-----|--------|
| `GET /` | `GET /api/dashboard/` | GET |

### Warehouse Management
| Old | New | Method |
|-----|-----|--------|
| `GET /lager-anlegen/` (form) | `POST /api/lager/` | POST |
| N/A | `GET /api/lager/` | GET |

### Item Management
| Old | New | Method |
|-----|-----|--------|
| `GET /artikel/` | `GET /api/artikel/` | GET |
| `GET /artikel-anlegen/` (form) | `POST /api/artikel/` | POST |
| `GET /artikel/<pk>/bearbeiten/` (form) | `PATCH /api/artikel/<pk>/` | PATCH |
| `POST /artikel/<pk>/loeschen/` | `DELETE /api/artikel/<pk>/` | DELETE |

### Order Management
| Old | New | Method |
|-----|-----|--------|
| `GET /bestellungen/` | `GET /api/bestellungen/` | GET |
| `GET /bestellung-anlegen/` (form) | `POST /api/bestellungen/` | POST |

### Goods Receipt
| Old | New | Method |
|-----|-----|--------|
| `POST /wareneingang/` (form) | `POST /api/wareneingang/` | POST |
| `POST /wareneingang-touch/` | `POST /api/wareneingang-touch/` | POST |

### Stock Management
| Old | New | Method |
|-----|-----|--------|
| `GET /bestandsauskunft/` | `GET /api/bestandsauskunft/` | GET |
| `POST /bestandskorrektur/` (form) | `POST /api/bestandskorrektur/` | POST |

### Import
| Old | New | Method |
|-----|-----|--------|
| `POST /import-excel/` (form) | `POST /api/import-excel/` | POST |

## Data Format Changes

### Old System (HTML Form)
```html
<form method="POST">
    <input name="name" value="Hauptlager">
    <input name="location" value="Berlin">
    <button type="submit">Submit</button>
</form>
```

### New System (JSON)
```json
{
  "name": "Hauptlager",
  "location": "Berlin"
}
```

## Response Format Changes

### Old System (HTML)
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Warehouses</h1>
    <ul>
        <li>Lager Nord - Hamburg</li>
        <li>Lager Süd - München</li>
    </ul>
</body>
</html>
```

### New System (JSON)
```json
[
  {
    "id": 1,
    "name": "Lager Nord",
    "location": "Hamburg"
  },
  {
    "id": 2,
    "name": "Lager Süd",
    "location": "München"
  }
]
```

## Security Comparison

### Old System
- ✅ CSRF protection via tokens
- ✅ Session-based authentication
- ❌ Requires server-side session storage
- ❌ Cookie-based (vulnerable to CSRF if not properly configured)
- ❌ Difficult to use from mobile apps or external services

### New System
- ✅ Stateless authentication
- ✅ No server-side session storage needed
- ✅ Token-based (protected from CSRF)
- ✅ Easy to use from any client (web, mobile, desktop)
- ✅ Fine-grained permission control
- ✅ Token expiration and refresh mechanism

## Migration Steps for Clients

### If You Were Using the Old System

1. **Update authentication**
   - Replace form-based login with API token login
   - Store access token securely
   - Include token in Authorization header

2. **Update data submission**
   - Convert HTML forms to JSON payloads
   - Use appropriate HTTP methods (POST, PUT, PATCH, DELETE)
   - Handle JSON responses

3. **Update error handling**
   - Parse JSON error responses
   - Handle authentication errors (401)
   - Handle validation errors (400)

### Example Migration: Creating a Warehouse

#### Old Code (Python/Requests with Session)
```python
import requests

session = requests.Session()

# Login (creates session cookie)
session.post('http://localhost:8000/login/', data={
    'username': 'admin',
    'password': 'pass',
    'csrfmiddlewaretoken': csrf_token
})

# Create warehouse (uses session cookie)
response = session.post('http://localhost:8000/lager-anlegen/', data={
    'name': 'Hauptlager',
    'location': 'Berlin',
    'csrfmiddlewaretoken': csrf_token
})
```

#### New Code (API with JWT)
```python
import requests

# Login (get JWT token)
login_response = requests.post('http://localhost:8000/api/token-login/', json={
    'username': 'admin',
    'password': 'pass'
})
token = login_response.json()['access']

# Create warehouse (use token)
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/lager/', 
    headers=headers,
    json={
        'name': 'Hauptlager',
        'location': 'Berlin'
    }
)
```

## Benefits of the New System

### For Developers
- ✅ Stateless architecture (easier to scale)
- ✅ RESTful design (industry standard)
- ✅ Easy to test with tools like curl, Postman
- ✅ Can be used by any client (web, mobile, desktop)
- ✅ No need to manage CSRF tokens

### For Users
- ✅ Faster responses (no HTML rendering)
- ✅ Can use any client application
- ✅ Better mobile app support
- ✅ More secure (proper token management)

### For Operations
- ✅ No server-side session storage needed
- ✅ Easier to scale horizontally
- ✅ Better caching possibilities
- ✅ Easier to implement CDN caching

## Backward Compatibility

The old HTML-based views have been completely removed in favor of the API. If you need HTML interfaces:

1. **Option 1**: Build a separate frontend (React, Vue, Angular) that consumes the API
2. **Option 2**: Use tools like Postman or Swagger UI for API exploration
3. **Option 3**: Build custom HTML pages that use JavaScript to call the API

## Common Questions

### Q: Can I still use a web browser?
A: Yes, but you'll need to:
- Use API testing tools (Postman, Insomnia)
- Build a frontend application that consumes the API
- Use browser extensions that can set custom headers

### Q: How do I handle token expiration?
A: Access tokens expire after 1 hour. Use the refresh token to get a new access token without requiring the user to log in again.

### Q: Is this more secure than cookies?
A: Yes, when implemented correctly:
- Tokens are not automatically sent with requests (prevents CSRF)
- Tokens can have shorter lifetimes
- No server-side session storage to compromise
- Fine-grained permission control

### Q: Can I use this with a mobile app?
A: Yes! JWT tokens are perfect for mobile apps. Store the token securely and include it in API requests.

### Q: What about the Django Admin?
A: The Django Admin still works with session-based authentication and is available at `/admin/`.

## Troubleshooting

### Issue: "Authentication credentials were not provided"
**Solution**: Ensure you're including the Authorization header:
```
Authorization: Bearer <your_access_token>
```

### Issue: "Token is invalid or expired"
**Solution**: Use the refresh token to get a new access token:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<your_refresh_token>"}'
```

### Issue: "CSRF verification failed"
**Solution**: API endpoints don't require CSRF tokens. If you're getting this error, you might be calling an old endpoint. Use the new API endpoints instead.

## Resources

- [JWT.io](https://jwt.io/) - Learn about JSON Web Tokens
- [Django REST Framework](https://www.django-rest-framework.org/) - API framework documentation
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) - JWT authentication

## Support

For questions or issues with the migration, refer to:
- README.md - General documentation
- API_TESTING_GUIDE.md - Detailed API usage
- API_OVERVIEW.md - Architecture and endpoint reference

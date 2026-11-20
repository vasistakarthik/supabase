# Swagger Documentation Workflow

## 1. Overview

In standard FastAPI installations, the `/docs` route attempts to fetch Swagger UI JavaScript and CSS bundles from external public CDNs (`cdn.jsdelivr.net` or `cdnjs.cloudflare.com`). In corporate or restricted networks, these public CDN requests are frequently blocked, intercepted, or slow, causing the documentation page to freeze or fail to load.

**WORKHUB** solves this with a **100% Offline & Localized Swagger Architecture** powered by `swagger_ui_bundle`.

---

## 2. Technical Implementation in `app/main.py`

### Disabling Default CDN Routes

Default CDN docs are disabled during app creation:

```python
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url=None,    # Disable automatic CDN /docs
    redoc_url=None    # Disable automatic CDN /redoc
)
```

### Local Static Asset Mounting

Swagger UI assets bundled inside Python site-packages are exposed locally:

```python
from swagger_ui_bundle import swagger_ui_path
from fastapi.staticfiles import StaticFiles

app.mount(
    "/swagger-ui",
    StaticFiles(directory=swagger_ui_path),
    name="swagger-ui"
)
```

### Custom Offline `/docs` Handler

```python
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        swagger_js_url="/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/swagger-ui/swagger-ui.css",
        swagger_favicon_url="data:image/x-icon;base64,iVBORw0KGgo="
    )
```

Notice:

- `swagger_js_url` points to local `/swagger-ui/swagger-ui-bundle.js` (1.06 MB).
- `swagger_css_url` points to local `/swagger-ui/swagger-ui.css` (145 KB).
- `swagger_favicon_url` uses an in-memory base64 data URI, preventing hanging calls to `fastapi.tiangolo.com`.

---

## 3. Swagger UI Interaction Flow

### 1. Generating OpenAPI Schema

When the browser loads `/docs`, the Swagger UI JavaScript requests `GET /openapi.json`. FastAPI automatically introspects:

- Every router endpoint (`/auth/register`, `/auth/login`, `/employees/`, etc.)
- All Pydantic request models and response models
- Security declarations (`HTTPBearer` in `app/core/security.py`)

### 2. Using the Authorize Modal

1. Register or Log in using `/auth/login` to obtain an `access_token`.
2. Click the green **Authorize 🔓** button at the top right of the Swagger UI.
3. In the **Value** box, paste the raw token (or `Bearer <token>`).
4. Click **Authorize** and then **Close**.
5. All locked endpoints (`/employees/*`) now automatically transmit the JWT in the `Authorization: Bearer <token>` header with every "Try it out" execution.

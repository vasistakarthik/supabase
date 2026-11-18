
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from swagger_ui_bundle import swagger_ui_path

from app.core.config import settings
from app.api.endpoints.employees import router as employee_router
from app.api.endpoints.auth import router as auth_router


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url=None,
    redoc_url=None
)

# Set OpenAPI version for Swagger UI compatibility
app.openapi_version = "3.0.3"


# Serve Swagger UI files locally
app.mount(
    "/swagger-ui",
    StaticFiles(directory=swagger_ui_path),
    name="swagger-ui"
)


# Custom Swagger documentation page
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():

    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        swagger_js_url="/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/swagger-ui/swagger-ui.css",
        swagger_favicon_url="data:image/x-icon;base64,iVBORw0KGgo="
    )


# Register Employee APIs
app.include_router(employee_router)

# Register Authentication APIs
app.include_router(auth_router)


# Home API
@app.get("/")
def home():

    return {
        "message": "Welcome to WORKHUB API",
        "status": "Running"
    }

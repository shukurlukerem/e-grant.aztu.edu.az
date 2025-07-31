from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

app = FastAPI(docs_url=None, redoc_url=None)  # Disable default docs

security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "secret123"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == USERNAME
    correct_password = credentials.password == PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/docs", include_in_schema=False)
def get_swagger_documentation(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure API Docs")

@app.get("/redoc", include_in_schema=False)
def get_redoc_documentation(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_redoc_html(openapi_url="/openapi.json", title="Secure API Docs")

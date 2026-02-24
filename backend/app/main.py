import os
from fastapi import FastAPI, HTTPException, Query, Header, Depends, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .store import InMemoryStore

app = FastAPI(title="Agent Sandbox", version="1.0.0")
store = InMemoryStore()

# ----------------------------
# Auth config (API Key)
# ----------------------------
# Define la API Key por variable de entorno para no hardcodear secretos.
# En local:  export API_KEY="agent-test-key"
# En Windows PowerShell:  setx API_KEY "agent-test-key"
API_KEY = os.getenv("API_KEY", "agent-test-key")
API_KEY_HEADER_NAME = "x-api-key"

def require_api_key(x_api_key: str | None = Header(default=None, alias=API_KEY_HEADER_NAME)):
    """
    Dependencia de FastAPI: valida que venga la API key en el header x-api-key.
    """
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")


# ----------------------------
# Static front (sin build)
# ----------------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


class CreateItem(BaseModel):
    title: str


@app.get("/")
def root():
    # El frontal NO requiere API key (para que puedas abrir la web en el navegador).
    return FileResponse("frontend/static/index.html")


@app.get("/api/health")
def health():
    # Health libre para checks sencillos / uptime / pruebas rápidas
    return {"status": "ok"}


# ----------------------------
# Protected API endpoints
# ----------------------------

@app.get("/api/items", dependencies=[Depends(require_api_key)])
def list_items(q: str | None = Query(default=None)):
    return {"items": store.list(q=q)}


@app.post("/api/items", status_code=201, dependencies=[Depends(require_api_key)])
def create_item(payload: CreateItem):
    try:
        return store.create(payload.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/items/{item_id}/toggle", dependencies=[Depends(require_api_key)])
def toggle_item(item_id: int):
    try:
        return store.toggle(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found")


@app.delete("/api/items/{item_id}", status_code=204, dependencies=[Depends(require_api_key)])
def delete_item(item_id: int):
    try:
        store.delete(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found")

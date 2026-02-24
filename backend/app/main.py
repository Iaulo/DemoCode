import os
from fastapi import FastAPI, HTTPException, Query, Header, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .store import InMemoryStore

app = FastAPI(title="Agent Sandbox", version="1.0.0")
store = InMemoryStore()

# ----------------------------
# Static front (sin build)
# ----------------------------
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


class CreateItem(BaseModel):
    title: str


@app.get("/")
def root():
    return FileResponse("frontend/static/index.html")


# ----------------------------
# Auth config (API Key) - OPTIONAL
# ----------------------------
# Por defecto: auth DESACTIVADA para que el frontal funcione sin tocar app.js.
# Para activarla: export REQUIRE_API_KEY=1
REQUIRE_API_KEY = os.getenv("REQUIRE_API_KEY", "0").lower() in ("1", "true", "yes", "on")

# API Key configurable
API_KEY = os.getenv("API_KEY", "agent-test-key")
API_KEY_HEADER_NAME = "x-api-key"


def require_api_key(x_api_key: str | None = Header(default=None, alias=API_KEY_HEADER_NAME)):
    """
    Si REQUIRE_API_KEY está activo, exige x-api-key correcto.
    Si no, deja pasar (modo demo).
    """
    if not REQUIRE_API_KEY:
        return

    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")


# ----------------------------
# Health
# ----------------------------
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "auth": "enabled" if REQUIRE_API_KEY else "disabled",
        "auth_type": "api-key-header" if REQUIRE_API_KEY else None,
        "header_name": API_KEY_HEADER_NAME if REQUIRE_API_KEY else None,
    }


# ----------------------------
# API endpoints (protegidos solo si REQUIRE_API_KEY=1)
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

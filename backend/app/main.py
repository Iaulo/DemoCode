from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .store import InMemoryStore

app = FastAPI(title="Agent Sandbox", version="1.0.0")
store = InMemoryStore()

# Sirve el frontal sin build
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


class CreateItem(BaseModel):
    title: str


@app.get("/")
def root():
    return FileResponse("frontend/static/index.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items(q: str | None = Query(default=None)):
    return {"items": store.list(q=q)}


@app.post("/api/items", status_code=201)
def create_item(payload: CreateItem):
    try:
        return store.create(payload.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/items/{item_id}/toggle")
def toggle_item(item_id: int):
    try:
        return store.toggle(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found")


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    try:
        store.delete(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="not found")

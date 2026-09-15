from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import engine, Base
from app.routers import projects

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BlueprintAgent API", version="1.0")

app.include_router(projects.router)

# Serve the chat frontend UI
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")
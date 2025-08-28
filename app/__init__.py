from fastapi import FastAPI
from .config import settings  
from .database import init_db 
from .routes import api_router  


def create_app() -> FastAPI:
    app = FastAPI(
        title="My FastAPI Backend",
        description="Backend API for my project",
        version="1.0.0",
    )

   
    init_db()

  
    app.include_router(api_router)

    return app



app = create_app()
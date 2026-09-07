from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.portfolios import router as portfolio_router
from app.api.routes.projects import router as project_router


app = FastAPI(
    title="Portfolio Engine API",
    description="Backend API for a dynamic, content-driven personal portfolio.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(portfolio_router)
app.include_router(project_router)


@app.get("/")
def root():
    return {
        "name": "Portfolio Engine API",
        "version": "0.1.0",
        "status": "running",
    }

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import analytics

app = FastAPI(title="ETL platform")
app.include_router(analytics.router)
add_pagination(app)

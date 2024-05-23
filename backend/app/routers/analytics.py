from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page, paginate
from starlette import status

from app.models.serialization.analytics import AnalyticsOut
from app.repositories.analytics import CloudProviders, TripAnalyticsRepository

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/analytics",
    description="Retrieve trip analytics",
    response_model=Page[AnalyticsOut],
)
def get_analytics(
    cloud_provider: Annotated[CloudProviders, Query(description="Cloud provider")],
    start_date: Annotated[date, Query(example="2023-01-01", description="Start date")],
    end_date: Annotated[date, Query(example="2024-01-01", description="End date")],
) -> list[AnalyticsOut]:
    analytics_repository = TripAnalyticsRepository(cloud_provider=cloud_provider)
    try:
        analytics_result = analytics_repository.get_analytics(start_date, end_date)
    except RuntimeError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return paginate(analytics_result)

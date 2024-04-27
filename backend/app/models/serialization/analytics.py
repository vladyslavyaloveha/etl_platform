from datetime import date

from pydantic import BaseModel


class AnalyticsOut(BaseModel):
    uuid: str
    date: date
    distance: float
    max_trip_distance: float
    passengers: int

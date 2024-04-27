from app.config.settings import get_settings
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

settings = get_settings()

SqlalchemyBase = declarative_base()


class TripAnalytics:
    uuid: Mapped[str] = Column(String, primary_key=True)
    date: Mapped[str] = Column(String)
    passengers: Mapped[str] = Column(String)
    distance: Mapped[str] = Column(String)
    max_trip_distance: Mapped[str] = Column(String)


class TripAnalyticsBigQuery(TripAnalytics, SqlalchemyBase):
    __tablename__ = f"{settings.bq_dataset_name}.{settings.table_name}"


class TripAnalyticsRedshift(TripAnalytics, SqlalchemyBase):
    __tablename__ = settings.table_name

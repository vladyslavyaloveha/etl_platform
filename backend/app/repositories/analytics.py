from datetime import date
from enum import Enum
from typing import Any

import sqlalchemy.exc
from sqlalchemy import and_, create_engine, select
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.models.orm.analytics import TripAnalyticsBigQuery, TripAnalyticsRedshift

settings = get_settings()


class CloudProviders(str, Enum):
    GCP = "Google Cloud Platform"
    AWS = "Amazon Web Services"


class TripAnalyticsRepository:
    """Repository for trip analytics analysis"""

    def __init__(self, cloud_provider: str) -> None:
        self._cloud_provider = cloud_provider
        self._session = self._get_session()
        self._model = self._get_model()

    def _get_session(self) -> Session:
        """Create sqlalchemy Session based on Cloud Provider"""
        match self._cloud_provider:
            case CloudProviders.GCP:
                engine = create_engine(
                    "bigquery://", credentials_path=settings.gcp_credentials_path
                )
            case CloudProviders.AWS:
                db_url = URL.create(
                    drivername="redshift+redshift_connector",
                    host=settings.redshift_host,
                    port=settings.redshift_port,
                    database=settings.redshift_database,
                    username=settings.redshift_master_username,
                    password=settings.redshift_master_password,
                )
                engine = create_engine(db_url)
            case _:
                raise ValueError(f"Invalid cloud provider: {self._cloud_provider}")
        return Session(engine)

    def _get_model(self) -> Any:
        """Get model based on given Cloud Provider"""
        match self._cloud_provider:
            case CloudProviders.GCP:
                return TripAnalyticsBigQuery
            case CloudProviders.AWS:
                return TripAnalyticsRedshift
            case _:
                raise ValueError(f"Invalid cloud provider: {self._cloud_provider}")

    def get_analytics(self, start_date: date, end_date: date) -> list[dict[str, Any]]:
        """Retrieves trip data analytics
        Args:
            start_date (date): Start date
            end_date (date): End date
        Returns:
            list[dict[str, Any]]: Trip analytics for provided date range
        """

        if start_date:
            start_date = start_date.strftime("%Y-%m-%d")
        if end_date:
            end_date = end_date.strftime("%Y-%m-%d")

        with self._session as session:
            statement = select(self._model).where(
                and_(self._model.date >= start_date, self._model.date <= end_date)
            )
            try:
                result = session.execute(statement).scalars().fetchall()
            except sqlalchemy.exc.DBAPIError as ex:
                raise RuntimeError(f"Unable to get data: {str(ex)}")
        return result

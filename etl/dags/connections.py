import json
from typing import Any

from airflow.decorators import task
from airflow.models import Connection
from sqlalchemy import update

from airflow import settings


@task(task_id="connection")
def create_connection(
    connection_id: str,
    connection_type: str,
    host: str | None = None,
    port: str | None = None,
    login: str | None = None,
    password: str | None = None,
    schema: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    """Create connection
    Args:
        connection_id (str): unique connection id
        connection_type (str): connection type
        host (str | None): host
        port (str | None): port
        login (str | None): login
        password (str | None): password
        schema (str | None): schema
        extra (dict[str, Any] | None): extra arguments related to connection
    Returns:
        None
    """

    with settings.Session() as session:
        connection = (
            session.query(Connection)
            .filter(Connection.conn_id == connection_id)
            .one_or_none()
        )
        if connection is None:
            connection = Connection(
                conn_id=connection_id,
                conn_type=connection_type,
                host=host,
                port=port,
                login=login,
                password=password,
                schema=schema,
                extra=extra,
            )
            session.add(connection)
        else:
            statement = (
                update(Connection)
                .where(Connection.conn_id == connection_id)
                .values(
                    {
                        "conn_id": connection_id,
                        "conn_type": connection_type,
                        "host": host,
                        "port": port,
                        "login": login,
                        "password": password,
                        "schema": schema,
                        "extra": json.dumps(extra) if extra else None,
                    }
                )
            )
            session.execute(statement)
        session.commit()

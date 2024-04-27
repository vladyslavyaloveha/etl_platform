import datetime
import os
import pathlib
import sys
import uuid
from pathlib import Path

import pandas as pd
import pyspark.sql
import pyspark.sql.functions as F
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


def to_datetime(date, date_format="%Y-%m-%d") -> datetime.datetime:
    return datetime.datetime.strptime(date, date_format)


def trip_analytics(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
    """Aggregated trip analytics by passenger_count, trip_distance, and date

    Args:
        df (pyspark.sql.DataFrame): Input dataframe
    Returns:
        pyspark.sql.DataFrame: Aggregated result
    """
    pickup_date_column = "tpep_pickup_date"
    df = df.withColumn(pickup_date_column, F.to_date(df["tpep_pickup_datetime"]))

    start_date = df.select(F.min(pickup_date_column)).collect()[0][0]
    end_date = df.select(F.max(pickup_date_column)).collect()[0][0]
    end_date = end_date + datetime.timedelta(days=1)

    filtered = df.filter(
        (df[pickup_date_column] >= start_date) & (df[pickup_date_column] < end_date)
    )
    if filtered.isEmpty():
        return filtered
    result = (
        filtered.groupby(pickup_date_column)
        .agg(
            F.round(F.sum("passenger_count"), 1).alias("passengers"),
            F.round(F.sum("trip_distance"), 2).alias("distance"),
            F.round(F.max("trip_distance"), 2).alias("max_trip_distance"),
        )
        .toPandas()
    )
    result.rename(columns={"tpep_pickup_date": "date"}, inplace=True)
    result["uuid"] = [str(uuid.uuid4()) for _ in range(len(result.index))]

    result["uuid"] = result["uuid"].astype(str)
    result["date"] = pd.to_datetime(result["date"]).dt.date
    result["passengers"] = result["passengers"].astype("int32")
    result["distance"] = result["distance"].astype(float)
    result["max_trip_distance"] = result["max_trip_distance"].astype(float)

    return result


if __name__ == "__main__":
    path = Path(sys.argv[1])
    spark = SparkSession(
        SparkContext(conf=SparkConf(), appName="transform").getOrCreate()
    )

    df = spark.read.parquet(str(path))
    result = trip_analytics(df)

    filename = f"analytics_{path.name[:-9]}"
    temp_filename = f"{str(uuid.uuid4())}_{filename}"

    save_path = pathlib.Path(path.parent).joinpath(filename).resolve()
    temp_path = pathlib.Path(path.parent).joinpath(temp_filename).resolve()
    result.to_parquet(temp_path)

    os.rename(temp_path, save_path)
    Path(path).unlink(missing_ok=True)

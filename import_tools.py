import logging
import os
from datetime import timedelta, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd
from dotenv import load_dotenv
from geoalchemy2 import Geometry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Flora

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))

Session = sessionmaker(bind=engine)

MUESTREO = Path("data/form-1__muestreo.csv")
BAIRES_TZ = timezone(timedelta(hours=-3))


def save_samples(gdf_samples, model=Flora):
    with Session() as session:
        record_exists = (
            session.query(model)
            .filter_by(
                field_date=str(gdf_samples.field_date[0]),
                file_name=gdf_samples.file_name[0],
            )
            .first()
        )
        if record_exists:
            logging.warning(
                f"Field {record_exists.field_date} from {record_exists.file_name} already saved on {model.__tablename__}"
            )
        else:
            gdf_samples.to_postgis(
                model.__tablename__,
                engine,
                if_exists="append",
                index=False,
                dtype={"geometry": Geometry(geometry_type="POINT", srid=4326)},
            )
            logging.warning(
                f"{model.__tablename__} saved: {gdf_samples.field_date[0]} from {gdf_samples.file_name[0]}"
            )


def import_samples(sample_path=MUESTREO):
    df_samples = pd.read_csv(sample_path)
    df_samples["file_name"] = sample_path.name
    gdf_samples = gpd.GeoDataFrame(
        df_samples,
        geometry=gpd.points_from_xy(df_samples["lon"], df_samples["lat"]),
        crs="EPSG:4326",
    )
    # convert the date time column to local timezone
    gdf_samples.created_at = pd.to_datetime(
        gdf_samples.created_at, utc=True
    ).dt.tz_convert(tz=BAIRES_TZ)
    gdf_samples.uploaded_at = pd.to_datetime(
        gdf_samples.uploaded_at, utc=True
    ).dt.tz_convert(tz=BAIRES_TZ)
    gdf_samples["field_date"] = gdf_samples.created_at.dt.date
    save_samples(
        gdf_samples,
        model=Flora,
    )

    return gdf_samples

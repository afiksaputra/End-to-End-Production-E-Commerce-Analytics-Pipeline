import os
import pandas as pd
from sqlalchemy import create_engine

def load_to_parquet(df: pd.DataFrame, file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_parquet(file_path, engine="pyarrow", index=False, compression="snappy")

def load_to_postgres(df: pd.DataFrame, table_name: str, db_url: str) -> None:
    engine = create_engine(db_url)
    with engine.begin() as connection:
        df.to_sql(name=table_name, con=connection, if_exists="append", index=False, method="multi")

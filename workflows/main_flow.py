import os
from prefect import task, flow
from src.extract.extract_data import fetch_raw_orders
from src.transform.transform_data import transform_orders, aggregate_daily_metrics
from src.load.load_data import load_to_parquet, load_to_postgres
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

@task(retries=2, retry_delay_seconds=3)
def extract_task(n): return fetch_raw_orders(n)

@task
def transform_task(data):
    clean_df = transform_orders(data)
    metrics_df = aggregate_daily_metrics(clean_df)
    return clean_df, metrics_df

@task
def load_task(clean_df, metrics_df):
    parquet_path = f"data/processed/orders_{clean_df['processing_date'].iloc[0]}.parquet"
    load_to_parquet(clean_df, parquet_path)
    load_to_postgres(metrics_df, "daily_sales_metrics", DB_URL)

@flow(name="Native Windows ETL Pipeline")
def main_etl_flow():
    raw_data = extract_task(300)
    clean_df, metrics_df = transform_task(raw_data)
    if not clean_df.empty:
        load_task(clean_df, metrics_df)

if __name__ == "__main__":
    main_etl_flow()

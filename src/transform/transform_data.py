import hashlib
import pandas as pd
from pydantic import BaseModel, Field, field_validator

class RawOrderSchema(BaseModel):
    order_id: str
    customer_name: str
    customer_email: str
    amount: float = Field(gt=0)
    payment_method: str
    status: str
    timestamp: str

    @field_validator('payment_method', mode='before')
    def default_payment_method(cls, v):
        return v if v is not None else "UNKNOWN"

def mask_pii(val: str) -> str:
    return hashlib.sha256(val.encode('utf-8')).hexdigest()

def transform_orders(raw_records: list[dict]) -> pd.DataFrame:
    validated = []
    for record in raw_records:
        try:
            valid = RawOrderSchema(**record).model_dump()
            valid["customer_email_hashed"] = mask_pii(valid["customer_email"])
            del valid["customer_email"]
            validated.append(valid)
        except Exception:
            continue
    df = pd.DataFrame(validated)
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["processing_date"] = pd.Timestamp.now().date()
    return df

def aggregate_daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    metrics = df.groupby(["processing_date", "payment_method", "status"]).agg(
        total_orders=('order_id', 'count'),
        total_revenue=('amount', 'sum'),
        avg_order_value=('amount', 'mean')
    ).reset_index()
    metrics["total_revenue"] = metrics["total_revenue"].round(2)
    metrics["avg_order_value"] = metrics["avg_order_value"].round(2)
    return metrics

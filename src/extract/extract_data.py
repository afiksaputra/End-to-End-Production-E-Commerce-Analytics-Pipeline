import random
import uuid
from datetime import datetime, timezone

def fetch_raw_orders(num_records: int = 100) -> list[dict]:
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    methods = ["CREDIT_CARD", "BANK_TRANSFER", "E_WALLET", None]
    raw_data = []
    for _ in range(num_records):
        raw_data.append({
            "order_id": str(uuid.uuid4()),
            "customer_name": f"User_{random.randint(100, 999)}",
            "customer_email": f"user{random.randint(1000, 9999)}@{random.choice(domains)}",
            "amount": round(random.uniform(-10.0, 1500.0), 2),
            "payment_method": random.choice(methods),
            "status": random.choice(["COMPLETED", "PENDING", "FAILED"]),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    return raw_data

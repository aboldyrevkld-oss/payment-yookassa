from fastapi im
port FastAPI, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import Base, engine, get_db
from app.utils import create_yookassa_payment, get_yookassa_payment
from app.crud import create_payment_record, get_payment, update_payment_status
from app.tasks import sync_all_payments

# Создаем таблицы при старте (если нужно)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payments YooKassa Service",
    description="YooKassa payments service with DB and Celery sync",
    version="1.0.0"
)

class PaymentRequest(BaseModel):
    amount: float
    description: str

class PaymentResponse(BaseModel):
    id: str
    amount: float
    description: str | None = None
    status: str
    confirmation_url: str | None = None

@app.post("/create-payment", response_model=PaymentResponse, summary="Create payment in YooKassa")
def create_payment(req: PaymentRequest, db: Session = Depends(get_db)):
    # Создаем платёж в YooKassa
    data = create_yookassa_payment(req.amount, req.description)
    payment_id = data["id"]
    status = data.get("status", "pending")
    confirmation = data.get("confirmation", {}) or {}
    confirmation_url = confirmation.get("confirmation_url")

    # Сохраняем в локальной БД
    create_payment_record(db, payment_id, req.amount, req.description, status)

    return PaymentResponse(
        id=payment_id,
        amount=req.amount,
        description=req.description,
        status=status,
        confirmation_url=confirmation_url
    )

@app.post("/webhook", summary="YooKassa webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    """
    Обрабатываем webhook от YooKassa.
    YooKassa пришлёт JSON с полем 'event' и 'object' (object — платеж).
    """
    body = await request.json()
    event = body.get("event")
    obj = body.get("object", {}) or {}
    payment_id = obj.get("id")
    status = obj.get("status")

    if payment_id and status:
        update_payment_status(db, payment_id, status)

    return {"received": True, "event": event, "payment_id": payment_id, "status": status}

@app.get("/payments/{payment_id}", response_model=PaymentResponse, summary="Get payment by id")
def get_payment_endpoint(payment_id: str, db: Session = Depends(get_db)):
    p = get_payment(db, payment_id)
    if not p:
        raise HTTPException(status_code=404, detail="Payment not found")
    return PaymentResponse(
        id=p.id,
        amount=p.amount,
        description=p.description,
        status=p.status,
        confirmation_url=None
    )

@app.post("/sync-payments", summary="Trigger sync of pending payments (schedules Celery tasks)")
def trigger_sync():
    task = sync_all_payments.delay()
    return {"task_id": task.id, "status": "scheduled"}

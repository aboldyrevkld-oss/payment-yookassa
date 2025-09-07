from sqlalchemy.orm import Session
from app.models import Payment

def create_payment_record(db: Session, payment_id: str, amount: float, de
                        scription: str, status: str, currency: str="RUB"):
    payment = Payment(
        id=payment_id,
        amount=amount,
        description=description,
        status=status,
        currency=currency
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def get_payment(db: Session, payment_id: str):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def update_payment_status(db: Session, payment_id: str, status: str):
    payment = get_payment(db, payment_id)
    if not payment:
        return None
    payment.status = status
    db.commit()
    db.refresh(payment)
    return payment

def list_pending_payments(db: Session):
    return db.query(Payment).filter(Payment.status.in_(["pending", "waiting_for_capture"])).all()  

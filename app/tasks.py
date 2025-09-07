from app.celery_app import celery
from app.db import SessionLocal
from app.crud import get_payment, update_payment_status, list_pending_payments
from app.utils import get_yookassa_payment

@celery.task(bind=True)
def sync_payment(self, payment_id: str):
    """
    Проверяет статус одного платежа и обновляет в БД.
    """
    db = SessionLocal()
    try:
        p = get_payment(db, payment_id)
        if not p:
            return {"ok": False, "msg": f"Payment {payment_id} not found"}

        data = get_yookassa_payment(payment_id)
        status = data.get("status")
        if status and p.status != status:
            updated = update_payment_status(db, payment_id, status)
            return {"ok": True, "msg": f"Updated {payment_id} → {status}"}
        return {"ok": True, "msg": f"No change for {payment_id} ({p.status})"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()

@celery.task(bind=True)
def sync_all_payments(self):
    """
    Находит все ожидающие/ждущие захвата платежи и ставит задачи sync_payment для каждого.
    """
    db = SessionLocal()
    try:
        pendings = list_pending_payments(db)
        count = 0
        for p in pendings:
            sync_payment.delay(p.id)
            count += 1
        return {"ok": True, "scheduled": count}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        db.close()

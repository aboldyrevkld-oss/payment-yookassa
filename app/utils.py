import requests
import uuid
from app.config import YOOKASSA_API_URL, YOOKASSA_SHOP_ID, YOOKASSA_API_KEY, YOOKASSA_SUCCESS_URL, YOOKASSA_CANCEL_URL

def create_yookassa_payment(amount: float, description: str, return_url: str = None):
    """
    Создаёт платёж в YooKassa. Возвращает JSON ответа YooKassa.
    """
    if return_url is None:
        return_url = YOOKASSA_SUCCESS_URL

    headers = {"Content-Type": "application/json"}
    auth = (YOOKASSA_SHOP_ID, YOOKASSA_API_KEY)

    payload = {
        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
        "capture": True,
        "description": description,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "metadata": {
            "local_id": str(uuid.uuid4())
        }
    }

    resp = requests.post(YOOKASSA_API_URL, json=payload, headers=headers, auth=auth, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_yookassa_payment(payment_id: str):
    """
    Получить информацию по id платежа в YooKassa.
    """
    auth = (YOOKASSA_SHOP_ID, YOOKASSA_API_KEY)
    resp = requests.get(f"{YOOKASSA_API_URL}/{payment_id}", auth=auth, timeout=10)
    resp.raise_for_status()
    return resp.json()

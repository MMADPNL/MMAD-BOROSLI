 # =========================================================
# BET BOT - payments.py
# Deposit / Withdraw System
# =========================================================

import uuid
from datetime import datetime


# درخواست‌های موقت پرداخت
pending_deposits = {}

pending_withdraws = {}


# =========================================================
# ساخت درخواست واریزی
# =========================================================

def create_deposit_request(
    user_id: int,
    amount: int,
    proof,
):

    request_id = str(uuid.uuid4())

    pending_deposits[request_id] = {

        "id": request_id,

        "user_id": user_id,

        "amount": amount,

        "proof": proof,

        "status": "pending",

        "created": datetime.now(),

    }

    return pending_deposits[request_id]


# =========================================================
# گرفتن درخواست واریزی
# =========================================================

def get_deposit(
    request_id: str,
):

    return pending_deposits.get(
        request_id
    )


# =========================================================
# تایید واریزی
# =========================================================

def approve_deposit(
    request_id: str,
):

    request = pending_deposits.get(
        request_id
    )

    if not request:
        return False


    if request["status"] != "pending":
        return False


    request["status"] = "approved"

    return request


# =========================================================
# رد واریزی
# =========================================================

def reject_deposit(
    request_id: str,
):

    request = pending_deposits.get(
        request_id
    )

    if not request:
        return False


    if request["status"] != "pending":
        return False


    request["status"] = "rejected"

    return request


# =========================================================
# ساخت برداشت
# =========================================================

def create_withdraw_request(
    user_id: int,
    amount: int,
):

    # حداقل برداشت
    if amount < 500:

        return False


    request_id = str(uuid.uuid4())


    pending_withdraws[request_id] = {

        "id": request_id,

        "user_id": user_id,

        "amount": amount,

        "status": "pending",

        "created": datetime.now(),

    }


    return pending_withdraws[request_id]


# =========================================================
# تایید برداشت
# =========================================================

def approve_withdraw(
    request_id: str,
):

    request = pending_withdraws.get(
        request_id
    )


    if not request:

        return False


    if request["status"] != "pending":

        return False


    request["status"] = "approved"


    return request



# =========================================================
# رد برداشت
# =========================================================

def reject_withdraw(
    request_id: str,
):

    request = pending_withdraws.get(
        request_id
    )


    if not request:

        return False


    if request["status"] != "pending":

        return False


    request["status"] = "rejected"


    return request



# =========================================================
# لیست درخواست‌های باز
# =========================================================

def get_pending_deposits():

    return [

        x for x in pending_deposits.values()

        if x["status"] == "pending"

    ]


def get_pending_withdraws():

    return [

        x for x in pending_withdraws.values()

        if x["status"] == "pending"

]

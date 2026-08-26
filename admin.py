# =========================================================
# BET BOT - admin.py
# Owner Panel
# =========================================================

from typing import Optional


# =========================================================
# تنظیمات مدیریت
# =========================================================

bot_status = True

owner_id = 8552447077


# =========================================================
# بررسی مالک
# =========================================================

def is_owner(user_id: int) -> bool:

    return user_id == owner_id



# =========================================================
# روشن / خاموش ربات
# =========================================================

def set_bot_status(
    status: bool
):

    global bot_status

    bot_status = status

    return bot_status



def get_bot_status():

    return bot_status



# =========================================================
# انتقال مالکیت
# =========================================================

def transfer_owner(
    current_owner: int,
    new_owner: int,
):

    global owner_id


    if current_owner != owner_id:

        return False


    if not isinstance(
        new_owner,
        int
    ):

        return False


    owner_id = new_owner


    return True



# =========================================================
# شارژ موجودی
# =========================================================

def admin_add_balance(
    database,
    user_id: int,
    amount: int,
):

    if amount <= 0:

        return False


    return database.add_balance(
        user_id,
        amount,
        "شارژ توسط مالک"
    )



# =========================================================
# کسر موجودی
# =========================================================

def admin_remove_balance(
    database,
    user_id: int,
    amount: int,
):

    if amount <= 0:

        return False


    return database.remove_balance(
        user_id,
        amount,
        "کسر توسط مالک"
    )



# =========================================================
# اطلاعات پنل
# =========================================================

def get_admin_info():

    return {

        "owner_id": owner_id,

        "status": (
            "روشن"
            if bot_status
            else "خاموش"
        )

    }

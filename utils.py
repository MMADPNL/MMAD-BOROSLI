# =========================================================
# BET BOT - utils.py
# Anti Bug / Security Tools
# =========================================================

import re
import time
import uuid
from functools import wraps


# =========================================================
# تبدیل عدد فارسی به انگلیسی
# =========================================================

def normalize_number(text):

    if not text:
        return None

    table = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    )

    return text.translate(table)



# =========================================================
# گرفتن عدد امن
# =========================================================

def safe_int(
    value,
    default=None
):

    try:

        value = normalize_number(
            str(value)
        )

        return int(value)

    except Exception:

        return default



# =========================================================
# بررسی مبلغ
# =========================================================

def valid_amount(
    amount
):

    if not isinstance(
        amount,
        int
    ):
        return False


    if amount <= 0:

        return False


    return True



# =========================================================
# ساخت شناسه یکتا
# =========================================================

def create_id():

    return str(
        uuid.uuid4()
    )



# =========================================================
# جلوگیری از اسپم
# =========================================================

_user_cooldowns = {}


def cooldown(
    seconds=3
):

    def decorator(func):

        @wraps(func)

        async def wrapper(
            update,
            context,
            *args,
            **kwargs
        ):

            user = update.effective_user


            if user:

                now = time.time()

                last = _user_cooldowns.get(
                    user.id,
                    0
                )


                if now - last < seconds:

                    if update.message:

                        await update.message.reply_text(
                            "⏳ لطفاً چند ثانیه صبر کنید."
                        )

                    return


                _user_cooldowns[user.id] = now



            return await func(
                update,
                context,
                *args,
                **kwargs
            )


        return wrapper


    return decorator



# =========================================================
# پاکسازی متن
# =========================================================

def clean_text(
    text
):

    if not text:

        return ""


    return (
        text
        .strip()
        .replace("\n", " ")
    )



# =========================================================
# بررسی دستور انتقال
# =========================================================

def parse_transfer(
    text
):

    if not text:

        return None


    text = normalize_number(
        text
    )


    match = re.match(
        r"انتقال\s+(\d+)",
        text
    )


    if not match:

        return None


    amount = int(
        match.group(1)
    )


    if amount <= 0:

        return None


    return amount



# =========================================================
# لاگ خطا
# =========================================================

def log_error(
    error
):

    print(
        "BOT ERROR:",
        error
              )

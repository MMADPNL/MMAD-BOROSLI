 # =========================================================
# BET BOT - referral.py
# Referral System
# Reward: 40 DOGS
# =========================================================

import re


# =========================================================
# تنظیمات
# =========================================================

REFERRAL_REWARD = 40


# =========================================================
# ساخت لینک زیرمجموعه
# =========================================================

def create_referral_link(
    bot_username: str,
    user_id: int,
):

    return (
        f"https://t.me/{bot_username}"
        f"?start=ref_{user_id}"
    )


# =========================================================
# گرفتن آیدی معرف از لینک
# =========================================================

def get_referrer_id(
    start_text: str,
):

    if not start_text:

        return None


    match = re.match(
        r"ref_(\d+)",
        start_text
    )


    if not match:

        return None


    return int(
        match.group(1)
    )


# =========================================================
# بررسی رفرال معتبر
# =========================================================

def validate_referral(
    referrer_id: int,
    new_user_id: int,
):

    # خودش را دعوت نکند

    if referrer_id == new_user_id:

        return False


    return True



# =========================================================
# ثبت رفرال و پرداخت جایزه
# =========================================================

def register_referral(
    database,
    referrer_id: int,
    new_user_id: int,
):

    if not validate_referral(
        referrer_id,
        new_user_id
    ):

        return False


    result = database.add_referral(
        referrer_id,
        new_user_id,
        REFERRAL_REWARD,
    )


    return result



# =========================================================
# متن نمایش زیرمجموعه
# =========================================================

def referral_text(
    count: int,
):

    return (
        "👥 زیرمجموعه شما\n\n"
        f"👤 تعداد دعوت‌ها: {count}\n"
        f"🎁 پاداش هر نفر: {REFERRAL_REWARD} DOGS"
  )

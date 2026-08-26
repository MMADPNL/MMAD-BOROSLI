 # =========================================================
# BET BOT - database.py
# Database / DOGS Balance
# =========================================================

import sqlite3
import threading
from typing import Optional


# =========================================================
# تنظیمات
# =========================================================

DB_NAME = "bet_bot.db"

_db_lock = threading.RLock()


# =========================================================
# اتصال به دیتابیس
# =========================================================

def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=30,
        check_same_thread=False,
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    return conn


# =========================================================
# ساخت جداول
# =========================================================

def init_db():

    with _db_lock:

        conn = get_connection()

        try:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT DEFAULT '',
                    first_name TEXT DEFAULT '',
                    balance INTEGER NOT NULL DEFAULT 0,
                    referrer_id INTEGER,
                    referral_paid INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    balance_before INTEGER NOT NULL,
                    balance_after INTEGER NOT NULL,
                    description TEXT DEFAULT '',
                    reference_id TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transfers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    chat_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    referred_id INTEGER NOT NULL UNIQUE,
                    reward INTEGER NOT NULL DEFAULT 40,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

        finally:

            conn.close()


# =========================================================
# ساخت / بروزرسانی کاربر
# =========================================================

def ensure_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
):

    with _db_lock:

        conn = get_connection()

        try:

            row = conn.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if row:

                conn.execute(
                    """
                    UPDATE users
                    SET username = ?,
                        first_name = ?
                    WHERE user_id = ?
                    """,
                    (
                        username or "",
                        first_name or "",
                        user_id,
                    ),
                )

            else:

                conn.execute(
                    """
                    INSERT INTO users
                    (
                        user_id,
                        username,
                        first_name
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        user_id,
                        username or "",
                        first_name or "",
                    ),
                )

            conn.commit()

        finally:

            conn.close()


# =========================================================
# دریافت اطلاعات کاربر
# =========================================================

def get_user(user_id: int):

    with _db_lock:

        conn = get_connection()

        try:

            return conn.execute(
                """
                SELECT *
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

        finally:

            conn.close()


# =========================================================
# دریافت موجودی
# =========================================================

def get_balance(user_id: int) -> int:

    ensure_user(user_id)

    with _db_lock:

        conn = get_connection()

        try:

            row = conn.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if not row:
                return 0

            return int(row["balance"])

        finally:

            conn.close()


# =========================================================
# تغییر موجودی
# =========================================================

def change_balance(
    user_id: int,
    amount: int,
    transaction_type: str,
    description: str = "",
    reference_id: Optional[str] = None,
) -> bool:

    if not isinstance(amount, int):

        return False

    ensure_user(user_id)

    with _db_lock:

        conn = get_connection()

        try:

            conn.execute("BEGIN IMMEDIATE")

            row = conn.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            ).fetchone()

            if not row:

                conn.rollback()
                return False

            old_balance = int(row["balance"])
            new_balance = old_balance + amount

            # جلوگیری از موجودی منفی
            if new_balance < 0:

                conn.rollback()
                return False

            # جلوگیری از ثبت دوباره تراکنش
            if reference_id:

                exists = conn.execute(
                    """
                    SELECT id
                    FROM transactions
                    WHERE reference_id = ?
                    """,
                    (reference_id,),
                ).fetchone()

                if exists:

                    conn.rollback()
                    return False

            conn.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
                """,
                (
                    new_balance,
                    user_id,
                ),
            )

            conn.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    balance_before,
                    balance_after,
                    description,
                    reference_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    transaction_type,
                    amount,
                    old_balance,
                    new_balance,
                    description,
                    reference_id,
                ),
            )

            conn.commit()

            return True

        except Exception:

            conn.rollback()
            return False

        finally:

            conn.close()


# =========================================================
# شارژ موجودی
# =========================================================

def add_balance(
    user_id: int,
    amount: int,
    description: str = "شارژ موجودی",
    reference_id: Optional[str] = None,
) -> bool:

    if amount <= 0:
        return False

    return change_balance(
        user_id=user_id,
        amount=amount,
        transaction_type="deposit",
        description=description,
        reference_id=reference_id,
    )


# =========================================================
# کسر موجودی
# =========================================================

def remove_balance(
    user_id: int,
    amount: int,
    description: str = "کسر موجودی",
    reference_id: Optional[str] = None,
) -> bool:

    if amount <= 0:
        return False

    return change_balance(
        user_id=user_id,
        amount=-amount,
        transaction_type="withdraw",
        description=description,
        reference_id=reference_id,
    )


# =========================================================
# انتقال DOGS
# =========================================================

def transfer_balance(
    sender_id: int,
    receiver_id: int,
    amount: int,
    chat_id: Optional[int] = None,
) -> bool:

    if amount <= 0:
        return False

    if sender_id == receiver_id:
        return False

    ensure_user(sender_id)
    ensure_user(receiver_id)

    with _db_lock:

        conn = get_connection()

        try:

            conn.execute("BEGIN IMMEDIATE")

            sender = conn.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (sender_id,),
            ).fetchone()

            receiver = conn.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (receiver_id,),
            ).fetchone()

            if not sender or not receiver:

                conn.rollback()
                return False

            sender_balance = int(
                sender["balance"]
            )

            receiver_balance = int(
                receiver["balance"]
            )

            # موجودی کافی نیست
            if sender_balance < amount:

                conn.rollback()
                return False

            new_sender_balance = (
                sender_balance - amount
            )

            new_receiver_balance = (
                receiver_balance + amount
            )

            conn.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
                """,
                (
                    new_sender_balance,
                    sender_id,
                ),
            )

            conn.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
                """,
                (
                    new_receiver_balance,
                    receiver_id,
                ),
            )

            conn.execute(
                """
                INSERT INTO transfers
                (
                    sender_id,
                    receiver_id,
                    amount,
                    chat_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    sender_id,
                    receiver_id,
                    amount,
                    chat_id,
                ),
            )

            transfer_id = conn.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]

            conn.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    balance_before,
                    balance_after,
                    description,
                    reference_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sender_id,
                    "transfer_out",
                    -amount,
                    sender_balance,
                    new_sender_balance,
                    f"انتقال به {receiver_id}",
                    f"transfer_out_{transfer_id}",
                ),
            )

            conn.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    balance_before,
                    balance_after,
                    description,
                    reference_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    receiver_id,
                    "transfer_in",
                    amount,
                    receiver_balance,
                    new_receiver_balance,
                    f"دریافت از {sender_id}",
                    f"transfer_in_{transfer_id}",
                ),
            )

            conn.commit()

            return True

        except Exception:

            conn.rollback()
            return False

        finally:

            conn.close()


# =========================================================
# ثبت زیرمجموعه
# =========================================================

def add_referral(
    referrer_id: int,
    referred_id: int,
    reward: int = 40,
) -> bool:

    if referrer_id == referred_id:
        return False

    if reward <= 0:
        return False

    ensure_user(referrer_id)
    ensure_user(referred_id)

    with _db_lock:

        conn = get_connection()

        try:

            conn.execute("BEGIN IMMEDIATE")

            # بررسی اینکه کاربر قبلاً رفرال شده یا نه
            exists = conn.execute(
                """
                SELECT id
                FROM referrals
                WHERE referred_id = ?
                """,
                (referred_id,),
            ).fetchone()

            if exists:

                conn.rollback()
                return False

            # بررسی اینکه خود کاربر قبلاً رفرر دارد یا نه
            user = conn.execute(
                """
                SELECT referrer_id
                FROM users
                WHERE user_id = ?
                """,
                (referred_id,),
            ).fetchone()

            if not user:

                conn.rollback()
                return False

            if user["referrer_id"] is not None:

                conn.rollback()
                return False

            conn.execute(
                """
                UPDATE users
                SET referrer_id = ?
                WHERE user_id = ?
                """,
                (
                    referrer_id,
                    referred_id,
                ),
            )

            conn.execute(
                """
                INSERT INTO referrals
                (
                    referrer_id,
                    referred_id,
                    reward
                )
                VALUES (?, ?, ?)
                """,
                (
                    referrer_id,
                    referred_id,
                    reward,
                ),
            )

            # پاداش فقط یک بار
            old_balance_row = conn.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (referrer_id,),
            ).fetchone()

            if not old_balance_row:

                conn.rollback()
                return False

            old_balance = int(
                old_balance_row["balance"]
            )

            new_balance = (
                old_balance + reward
            )

            conn.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
                """,
                (
                    new_balance,
                    referrer_id,
                ),
            )

            conn.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    type,
                    amount,
                    balance_before,
                    balance_after,
                    description,
                    reference_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    referrer_id,
                    "referral",
                    reward,
                    old_balance,
                    new_balance,
                    f"پاداش رفرال {referred_id}",
                    f"referral_{referred_id}",
                ),
            )

            conn.commit()

            return True

        except Exception:

            conn.rollback()
            return False

        finally:

            conn.close()


# =========================================================
# تعداد زیرمجموعه‌ها
# =========================================================

def get_referral_count(
    user_id: int,
) -> int:

    with _db_lock:

        conn = get_connection()

        try:

            row = conn.execute(
                """
                SELECT COUNT(*) AS total
                FROM referrals
                WHERE referrer_id = ?
                """,
                (user_id,),
            ).fetchone()

            return int(row["total"])

        finally:

            conn.close()


# =========================================================
# تراکنش‌های اخیر کاربر
# =========================================================

def get_transactions(
    user_id: int,
    limit: int = 20,
):

    if limit <= 0:
        limit = 20

    if limit > 100:
        limit = 100

    with _db_lock:

        conn = get_connection()

        try:

            return conn.execute(
                """
                SELECT *
                FROM transactions
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    user_id,
                    limit,
                ),
            ).fetchall()

        finally:

            conn.close()


# =========================================================
# اجرای اولیه دیتابیس
# =========================================================

init_db()

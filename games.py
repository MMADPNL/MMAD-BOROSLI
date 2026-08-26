 # =========================================================
# BET BOT - games.py
# Games Engine
# Dice / Bowling / Football / Dart / Basketball
# =========================================================

import random
import uuid
from datetime import datetime


# =========================================================
# بازی‌های فعال
# =========================================================

active_games = {}


# =========================================================
# ساخت بازی
# =========================================================

def create_game(
    owner_id: int,
    game_type: str,
    amount: int,
    chat_id: int,
):

    game_id = str(uuid.uuid4())

    game = {
        "id": game_id,
        "owner": owner_id,
        "player2": None,
        "game": game_type,
        "amount": amount,
        "chat_id": chat_id,
        "status": "waiting",
        "created": datetime.now(),
        "owner_score": None,
        "player2_score": None,
    }

    active_games[game_id] = game

    return game


# =========================================================
# ورود بازیکن دوم
# =========================================================

def join_game(
    game_id: str,
    user_id: int,
):

    game = active_games.get(game_id)

    if not game:
        return False, "بازی پیدا نشد."

    if game["status"] != "waiting":
        return False, "این بازی شروع شده است."

    if game["owner"] == user_id:
        return False, "نمی‌توانید وارد بازی خودتان شوید."

    game["player2"] = user_id
    game["status"] = "playing"

    return True, game


# =========================================================
# بازی با ربات
# =========================================================

def play_with_bot(
    game_type: str,
    user_score: int,
):

    bot_score = generate_score(game_type)

    result = compare_scores(
        user_score,
        bot_score,
    )

    return {
        "user": user_score,
        "bot": bot_score,
        "result": result,
    }


# =========================================================
# انداختن بازی
# =========================================================

def generate_score(game_type: str):

    if game_type == "dice":

        return random.randint(
            1,
            6,
        )


    if game_type == "bowling":

        return random.randint(
            0,
            10,
        )


    if game_type == "football":

        return random.randint(
            0,
            5,
        )


    if game_type == "dart":

        return random.randint(
            0,
            60,
        )


    if game_type == "basketball":

        return random.randint(
            0,
            100,
        )


    return 0


# =========================================================
# مقایسه نتیجه
# =========================================================

def compare_scores(
    player1,
    player2,
):

    if player1 > player2:

        return "player1_win"


    if player2 > player1:

        return "player2_win"


    return "draw"


# =========================================================
# پایان بازی
# =========================================================

def finish_game(
    game_id: str,
    score1: int,
    score2: int,
):

    game = active_games.get(game_id)

    if not game:
        return None


    game["owner_score"] = score1
    game["player2_score"] = score2

    result = compare_scores(
        score1,
        score2,
    )


    game["status"] = "finished"


    # پاک کردن بازی بعد از پایان
    # نتیجه قبل از حذف قابل استفاده است

    return {
        "game": game,
        "result": result,
    }


# =========================================================
# لغو بازی
# =========================================================

def cancel_game(
    game_id: str,
    user_id: int,
):

    game = active_games.get(game_id)

    if not game:
        return False


    if game["owner"] != user_id:
        return False


    del active_games[game_id]

    return True


# =========================================================
# گرفتن بازی‌های منتظر
# =========================================================

def get_waiting_games(
    chat_id: int = None,
):

    games = []

    for game in active_games.values():

        if game["status"] == "waiting":

            if chat_id is None or game["chat_id"] == chat_id:

                games.append(game)


    return games


# =========================================================
# جایزه بازی
# =========================================================

def calculate_reward(
    amount: int,
):

    # 200 سهم مالک
    # 1800 به برنده در مثال شرط 1000

    owner_fee = int(
        amount * 0.20
    )

    winner_reward = (
        amount * 2
        - owner_fee
    )

    return {
        "winner": winner_reward,
        "owner": owner_fee,
  }

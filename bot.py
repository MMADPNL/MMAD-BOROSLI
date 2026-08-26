# =========================================================
# BET BOT - bot.py
# Python 3.10+
# python-telegram-bot 20+
# =========================================================

import logging
import re

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# =========================================================
# 🔑 تنظیمات اصلی
# =========================================================

TOKEN = "7851160438:AAEre2pDD-A_TGfoKPJeidFMnm6OIQB2v5s"

# 👑 آیدی عددی مالک
OWNER_ID = 8552447077


# =========================================================
# 🛡️ LOG
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("BET_BOT")


# =========================================================
# 🔢 تبدیل اعداد فارسی و عربی به انگلیسی
# =========================================================

def normalize_digits(text: str) -> str:

    table = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )

    return text.translate(table)


# =========================================================
# 🏠 منوی اصلی
# =========================================================

def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "💸 برداشت",
                callback_data="withdraw",
            ),
            InlineKeyboardButton(
                "💰 واریزی",
                callback_data="deposit",
            ),
        ],

        [
            InlineKeyboardButton(
                "💳 موجودی",
                callback_data="balance",
            ),
            InlineKeyboardButton(
                "👥 زیرمجموعه",
                callback_data="referral",
            ),
        ],

        [
            InlineKeyboardButton(
                "🎮 بازی‌ها",
                callback_data="games",
            ),
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# 🎮 منوی بازی‌ها
# =========================================================

def games_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🎲 تاس",
                callback_data="game_dice",
            ),
            InlineKeyboardButton(
                "🎳 بولینگ",
                callback_data="game_bowling",
            ),
        ],

        [
            InlineKeyboardButton(
                "⚽ فوتبال",
                callback_data="game_football",
            ),
            InlineKeyboardButton(
                "🎯 دارت",
                callback_data="game_dart",
            ),
        ],

        [
            InlineKeyboardButton(
                "🏀 بسکتبال",
                callback_data="game_basketball",
            ),
        ],

        [
            InlineKeyboardButton(
                "🔙 برگشت",
                callback_data="home",
            ),
        ],

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# 🚀 START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    user = update.effective_user

    # پاک کردن وضعیت قبلی
    context.user_data.clear()

    username = (
        f"@{user.username}"
        if user.username
        else "ندارد"
    )

    text = (
        "🎰 <b>BET BOT</b>\n\n"

        f"👤 {user.first_name}\n"
        f"🆔 آیدی عددی: <code>{user.id}</code>\n"
        f"🔹 یوزرنیم: {username}\n\n"

        "💰 واحد حساب: DOGS\n\n"

        "🎮 بازی‌ها:\n"
        "🎲 تاس\n"
        "🎳 بولینگ\n"
        "⚽ فوتبال\n"
        "🎯 دارت\n"
        "🏀 بسکتبال\n\n"

        "از منوی زیر انتخاب کنید:"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# =========================================================
# 🔘 مدیریت دکمه‌ها
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if not query:
        return

    try:
        await query.answer()
    except Exception:
        pass

    data = query.data
    user = query.from_user


    # =====================================================
    # 🏠 خانه
    # =====================================================

    if data == "home":

        await query.message.reply_text(
            "🏠 <b>منوی اصلی</b>",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

        return


    # =====================================================
    # 💸 برداشت
    # =====================================================

    if data == "withdraw":

        context.user_data["state"] = "withdraw_amount"

        await query.message.reply_text(
            "💸 <b>برداشت DOGS</b>\n\n"

            "تعداد DOGS را وارد کنید.\n\n"

            "🔻 حداقل برداشت: <b>500 DOGS</b>\n\n"

            "مثال:\n"
            "<code>1000</code>\n"
            "یا\n"
            "<code>۱۰۰۰</code>",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 💰 واریزی
    # =====================================================

    if data == "deposit":

        context.user_data["state"] = "deposit_amount"

        await query.message.reply_text(
            "💰 <b>واریزی DOGS</b>\n\n"

            "ابتدا تعداد DOGS واریزی را وارد کنید.\n\n"

            "مثال:\n"
            "<code>100</code>\n"
            "یا\n"
            "<code>۱۰۰</code>",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 💳 موجودی
    # =====================================================

    if data == "balance":

        username = (
            f"@{user.username}"
            if user.username
            else "ندارد"
        )

        await query.message.reply_text(
            "💳 <b>موجودی شما</b>\n\n"

            f"👤 یوزرنیم: {username}\n"
            f"🆔 آیدی عددی: <code>{user.id}</code>\n\n"

            "💰 موجودی DOGS: <b>0</b>",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 👥 زیرمجموعه
    # =====================================================

    if data == "referral":

        bot_username = context.bot.username

        if not bot_username:
            bot_username = "YourBot"

        referral_link = (
            f"https://t.me/{bot_username}"
            f"?start=ref_{user.id}"
        )

        await query.message.reply_text(
            "👥 <b>سیستم زیرمجموعه</b>\n\n"

            "🔗 لینک اختصاصی شما:\n"
            f"<code>{referral_link}</code>\n\n"

            "🎁 پاداش هر رفرال موفق:\n"
            "<b>40 DOGS</b>",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 🎮 بازی‌ها
    # =====================================================

    if data == "games":

        await query.message.reply_text(
            "🎮 <b>بازی موردنظر را انتخاب کنید:</b>",
            parse_mode="HTML",
            reply_markup=games_menu(),
        )

        return


    # =====================================================
    # 🎲 انتخاب بازی
    # =====================================================

    game_names = {

        "game_dice": "🎲 تاس",
        "game_bowling": "🎳 بولینگ",
        "game_football": "⚽ فوتبال",
        "game_dart": "🎯 دارت",
        "game_basketball": "🏀 بسکتبال",

    }


    if data in game_names:

        game = game_names[data]

        game_word = game.split(" ", 1)[1]

        await query.message.reply_text(
            f"{game}\n\n"

            "برای ساخت بازی داخل گپ بنویسید:\n\n"

            f"<code>1 {game_word} 1000</code>\n"
            f"<code>1 {game_word} ۱۰۰۰</code>\n\n"

            "⚠️ سیستم بازی در فایل بازی‌ها فعال می‌شود.",
            
            parse_mode="HTML",
        )

        return


# =========================================================
# 📝 مدیریت پیام‌های متنی
# =========================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    text = update.message.text

    if not text:
        return

    text = text.strip()

    if not text:
        return

    normalized = normalize_digits(text)

    state = context.user_data.get("state")


    # =====================================================
    # 💸 برداشت
    # =====================================================

    if state == "withdraw_amount":

        if not normalized.isdigit():

            await update.message.reply_text(
                "❌ فقط عدد وارد کنید.\n\n"
                "مثال:\n"
                "500"
            )

            return

        amount = int(normalized)


        if amount < 500:

            await update.message.reply_text(
                "❌ حداقل برداشت 500 DOGS است."
            )

            return


        context.user_data["withdraw_amount"] = amount

        context.user_data["state"] = None


        await update.message.reply_text(
            f"💸 درخواست برداشت <b>{amount:,} DOGS</b> ثبت شد.\n\n"
            "⏳ درخواست برای مالک ارسال خواهد شد.",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 💰 مبلغ واریزی
    # =====================================================

    if state == "deposit_amount":

        if not normalized.isdigit():

            await update.message.reply_text(
                "❌ فقط عدد وارد کنید.\n\n"
                "مثال:\n"
                "100"
            )

            return


        amount = int(normalized)


        if amount <= 0:

            await update.message.reply_text(
                "❌ مبلغ باید بیشتر از صفر باشد."
            )

            return


        context.user_data["deposit_amount"] = amount

        context.user_data["state"] = "deposit_proof"


        await update.message.reply_text(
            "💰 <b>فرمت واریزی</b>\n\n"

            f"<code>ULTRA {amount} DOGS @MMAD_Tek</code>\n\n"

            "📸 حالا شات یا پیام واریزی را ارسال کنید.\n\n"

            "✅ شات قبول است.\n"
            "✅ پیام واریزی هم قبول است.",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 📸 مدرک واریزی
    # =====================================================

    if state == "deposit_proof":

        amount = context.user_data.get(
            "deposit_amount"
        )

        if not amount:

            context.user_data.clear()

            await update.message.reply_text(
                "❌ درخواست واریزی نامعتبر است.\n"
                "لطفاً دوباره از منوی واریزی شروع کنید."
            )

            return


        # فعلاً ثبت اولیه درخواست
        # سیستم ارسال برای مالک در payments.py اضافه می‌شود

        context.user_data.clear()


        await update.message.reply_text(
            "📨 مدرک واریزی دریافت شد.\n\n"

            f"💰 مبلغ: <b>{amount:,} DOGS</b>\n"

            "⏳ درخواست برای مالک ارسال می‌شود.\n\n"

            "بعد از تأیید مالک، موجودی شما اضافه خواهد شد.",
            
            parse_mode="HTML",
        )

        return


    # =====================================================
    # 🔄 انتقال در گپ
    # =====================================================

    if update.message.chat.type in (
        "group",
        "supergroup",
    ):

        transfer_match = re.fullmatch(
            r"انتقال\s+([0-9]+)",
            normalized,
        )


        if transfer_match:

            amount = int(
                transfer_match.group(1)
            )


            # ---------------------------------------------
            # مبلغ نامعتبر
            # ---------------------------------------------

            if amount <= 0:

                await update.message.reply_text(
                    "❌ مبلغ باید بیشتر از صفر باشد."
                )

                return


            # ---------------------------------------------
            # باید ریپلای باشد
            # ---------------------------------------------

            if not update.message.reply_to_message:

                await update.message.reply_text(
                    "❌ انتقال باید با ریپلای انجام شود.\n\n"

                    "مثال:\n"
                    "<code>انتقال 100</code>\n"
                    "یا\n"
                    "<code>انتقال ۱۰۰</code>",
                    
                    parse_mode="HTML",
                )

                return


            target = (
                update.message
                .reply_to_message
                .from_user
            )


            # ---------------------------------------------
            # انتقال به خود
            # ---------------------------------------------

            if target.id == update.effective_user.id:

                await update.message.reply_text(
                    "❌ نمی‌توانید به خودتان انتقال دهید."
                )

                return


            # ---------------------------------------------
            # فعلاً انتقال آزمایشی
            # دیتابیس در database.py اضافه می‌شود
            # ---------------------------------------------

            await update.message.reply_text(
                "🔄 <b>درخواست انتقال</b>\n\n"

                f"💰 مبلغ: <b>{amount:,} DOGS</b>\n"
                f"👤 گیرنده: <b>{target.first_name}</b>\n\n"

                "⏳ سیستم موجودی در فایل دیتابیس فعال می‌شود.",
                
                parse_mode="HTML",
            )

            return


# =========================================================
# 🛡️ مدیریت خطا
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):

    logger.error(
        "BOT ERROR: %s",
        context.error,
        exc_info=True,
    )


# =========================================================
# 🚀 اجرای ربات
# =========================================================

def main():

    if not TOKEN:

        raise RuntimeError(
            "توکن ربات را در متغیر TOKEN قرار دهید."
        )


    application = (
        Application.builder()
        .token(TOKEN)
        .build()
    )


    # /start
    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )


    # دکمه‌ها
    application.add_handler(
        CallbackQueryHandler(
            button_handler,
        )
    )


    # پیام‌های متنی
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler,
        )
    )


    # خطا
    application.add_error_handler(
        error_handler
    )


    print("======================================")
    print("🚀 BET BOT STARTED")
    print(f"👑 OWNER ID: {OWNER_ID}")
    print("💰 CURRENCY: DOGS")
    print("======================================")


    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()

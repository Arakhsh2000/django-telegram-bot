from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from users.models import User

# Conversation steps
ASK_USERNAME, ASK_PASSWORD = range(2)

# Admin info
ADMIN_USERNAME = "Arakhsh00"
ADMIN_ID = 998716460


def ask_username(update: Update, context: CallbackContext):
    welcome_message = (
        "سلام وقت بخیر ☀️\n\n"
        "برای فعال‌سازی اکانت پلاس، لطفاً *نام کاربری* و *رمز عبور* اکانتی که مد نظرتون هست رو از طریق فرم زیر برای ما ارسال کنید.\n\n"
        "✅ می‌تونید اکانت فعلی‌تون رو ارسال کنید یا یک ایمیل و اکانت جدید بسازید و اون رو وارد کنید.\n\n"
        "💳 سپس با استفاده از لینک پرداخت زیر، مبلغ را پرداخت کنید.\n"
        "🧾 حتماً اسکرین‌شات یا رسید پرداخت را برای ادمین ارسال نمایید.\n\n"
        "حالا لطفاً *نام کاربری* مورد نظر را وارد کنید:"
    )
    update.message.reply_text(welcome_message, parse_mode="Markdown")
    return ASK_USERNAME


def ask_password(update: Update, context: CallbackContext):
    context.user_data["username"] = update.message.text.strip()
    update.message.reply_text("🔒 حالا لطفاً *رمز عبور* خود را وارد کنید:", parse_mode="Markdown")
    return ASK_PASSWORD


def finish(update: Update, context: CallbackContext):
    password = update.message.text.strip()
    username = context.user_data["username"]
    telegram_id = update.effective_user.id
    telegram_name = update.effective_user.full_name

    # Save to context
    context.user_data["password"] = password

    # Save to database
    User.objects.update_or_create(
        user_id=telegram_id,
        defaults={"username": username, "password": password}
    )

    # Message for user to forward
    confirmation_msg = (
        "✅ اطلاعات ثبت‌شده:\n\n"
        f"*نام کاربری:* `{username}`\n"
        f"*رمز عبور:* `{password}`\n\n"
        "💬 لطفاً این پیام را همراه با *رسید یا اسکرین‌شات پرداخت* برای ادمین فوروارد کنید:\n"
        f"👉 @{ADMIN_USERNAME}"
    )
    update.message.reply_text(confirmation_msg, parse_mode="Markdown")

    # Payment link
    update.message.reply_text(
        "💳 لینک پرداخت:\n"
        "https://revolut.me/r/cIWIoA4PW5\n\n"
        "✅ بعد از پرداخت، پیام بالا + رسید را برای ادمین ارسال کنید تا فعال‌سازی انجام شود.",
        parse_mode="Markdown"
    )

    # Backup admin notification
    admin_msg = (
        "📥 *درخواست جدید دریافت شد!*\n\n"
        f"*نام:* {telegram_name}\n"
        f"*Username:* `{username}`\n"
        f"*Password:* `{password}`\n"
        f"*Telegram ID:* `{telegram_id}`\n"
        f"[پاسخ به کاربر](tg://user?id={telegram_id})"
    )
    context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")

    return ConversationHandler.END

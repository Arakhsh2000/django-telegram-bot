# from telegram import Update
# from telegram.ext import CallbackContext, ConversationHandler
# from users.models import User

# # Conversation steps
# ASK_USERNAME, ASK_PASSWORD = range(2)

# # Admin info
# ADMIN_USERNAME = "GPadmin_A"  # your Telegram username
# ADMIN_ID = 998716460          # your numeric Telegram ID


# def ask_username(update: Update, context: CallbackContext):
#     welcome_message = (
#         "سلام وقت بخیر ☀️\n\n"
#         "برای فعال‌سازی اکانت پلاس، لطفاً <b>نام کاربری</b> و <b>رمز عبور</b> اکانتی که مد نظرتون هست رو از طریق فرم زیر برای ما ارسال کنید.\n\n"
#         "✅ می‌تونید اکانت فعلی‌تون رو ارسال کنید یا یک ایمیل و اکانت جدید بسازید و اون رو وارد کنید.\n\n"
#         "💳 سپس با استفاده از لینک پرداخت زیر، مبلغ را پرداخت کنید.\n"
#         "🧾 حتماً اسکرین‌شات یا رسید پرداخت را برای ادمین ارسال نمایید.\n\n"
#         "حالا لطفاً <b>نام کاربری</b> مورد نظر را وارد کنید:"
#     )
#     update.message.reply_text(welcome_message, parse_mode="HTML")
#     return ASK_USERNAME


# def ask_password(update: Update, context: CallbackContext):
#     context.user_data["username"] = update.message.text.strip()
#     update.message.reply_text("🔒 حالا لطفاً <b>رمز عبور</b> خود را وارد کنید:", parse_mode="HTML")
#     return ASK_PASSWORD


# def finish(update: Update, context: CallbackContext):
#     password = update.message.text.strip()
#     username = context.user_data["username"]
#     telegram_id = update.effective_user.id
#     telegram_name = update.effective_user.full_name

#     context.user_data["password"] = password

#     # Save to database
#     User.objects.update_or_create(
#         user_id=telegram_id,
#         defaults={"username": username, "password": password}
#     )

#     # Message for user to forward
#     confirmation_msg = (
#         "✅ <b>اطلاعات ثبت‌شده:</b>\n\n"
#         f"<b>نام کاربری:</b> <code>{username}</code>\n"
#         f"<b>رمز عبور:</b> <code>{password}</code>\n\n"
#         f"💬 لطفاً این پیام را همراه با <b>رسید یا اسکرین‌شات پرداخت</b> برای ادمین فوروارد کنید:\n"
#         f"👉 @{ADMIN_USERNAME}"
#     )
#     update.message.reply_text(confirmation_msg, parse_mode="HTML")

#     # Payment link
#     update.message.reply_text(
#         "💳 <b>لینک پرداخت:</b>\n"
#         "https://revolut.me/r/cIWIoA4PW5\n\n"
#         "✅ بعد از پرداخت، پیام بالا + رسید را برای ادمین ارسال کنید تا فعال‌سازی انجام شود.",
#         parse_mode="HTML"
#     )

#     # Backup admin notification
#     admin_msg = (
#         "📥 <b>درخواست جدید دریافت شد!</b>\n\n"
#         f"<b>نام:</b> {telegram_name}\n"
#         f"<b>Username:</b> <code>{username}</code>\n"
#         f"<b>Password:</b> <code>{password}</code>\n"
#         f"<b>Telegram ID:</b> <code>{telegram_id}</code>\n"
#         f"<a href='tg://user?id={telegram_id}'>پاسخ به کاربر</a>"
#     )
#     context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")

#     return ConversationHandler.END

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from users.models import User

# Conversation steps
ASK_USERNAME, ASK_PASSWORD = range(2)

# Admin info
ADMIN_USERNAME = "GPadmin_A"  # your Telegram username
ADMIN_ID = 998716460          # your numeric Telegram ID

def ask_username(update: Update, context: CallbackContext):
    welcome_message = (
        "سلام وقت بخیر ☀️\n\n"
        "برای فعال‌سازی اکانت پلاس، لطفاً <b>نام کاربری</b> و <b>رمز عبور</b> اکانتی که مد نظرتون هست رو از طریق فرم زیر برای ما ارسال کنید.\n\n"
        "✅ می‌تونید اکانت فعلی‌تون  چت جی‌پی‌تی ‌را ارسال کنید یا یک ایمیل جدید اکانت جدید چت جی‌پی تی بسازید و اون رو وارد کنید.\n\n"
        "💳 سپس با استفاده از لینک پرداخت زیر، مبلغ را پرداخت کنید.\n"
        "🧾 حتماً اسکرین‌شات یا رسید پرداخت را برای ادمین ارسال نمایید.\n\n"
        "حالا لطفاً <b>نام کاربری</b> مورد نظر را وارد کنید:"
    )
    update.message.reply_text(welcome_message, parse_mode="HTML")
    return ASK_USERNAME

def ask_password(update: Update, context: CallbackContext):
    context.user_data["username"] = update.message.text.strip()
    update.message.reply_text("🔒 حالا لطفاً <b>رمز عبور</b> خود را وارد کنید:", parse_mode="HTML")
    return ASK_PASSWORD

def finish(update: Update, context: CallbackContext):
    password = update.message.text.strip()
    username = context.user_data["username"]
    telegram_id = update.effective_user.id
    telegram_name = update.effective_user.full_name

    context.user_data["password"] = password

    # Save to database — includes password (now safe because you updated your model)
    User.objects.update_or_create(
        user_id=telegram_id,
        defaults={"username": username, "password": password}
    )

    # Message for user to forward
    confirmation_msg = (
        "✅ <b>اطلاعات ثبت‌شده:</b>\n\n"
        f"<b>نام کاربری:</b> <code>{username}</code>\n"
        f"<b>رمز عبور:</b> <code>{password}</code>\n\n"
        f"💬 لطفاً این پیام را همراه با <b>رسید یا اسکرین‌شات پرداخت</b> برای ادمین فوروارد کنید:\n"
        f"👉 @{ADMIN_USERNAME}"
    )
    update.message.reply_text(confirmation_msg, parse_mode="HTML")

    # Payment link
    update.message.reply_text(
    "💳 <b>لطفاً مبلغ <u>8.99 یورو</u> را به حساب رولوت زیر واریز کنید:</b>\n"
    "<b>لینک پرداخت:</b> <a href=\"https://revolut.me/arashsv36\">https://revolut.me/arashsv36</a>\n\n"
    "برای پرداخت کافی است روی لینک بالا بزنید یا در اپلیکیشن ریولوت، این آیدی را جستجو کنید: <code>arashsv36</code>\n\n"
    "✅ بعد از پرداخت، پیام بالا + رسید را برای ادمین ارسال کنید تا فعال‌سازی انجام شود.",
    parse_mode="HTML"
)

    # Backup admin notification
    admin_msg = (
        "📥 <b>درخواست جدید دریافت شد!</b>\n\n"
        f"<b>نام:</b> {telegram_name}\n"
        f"<b>Username:</b> <code>{username}</code>\n"
        f"<b>Password:</b> <code>{password}</code>\n"
        f"<b>Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<a href='tg://user?id={telegram_id}'>پاسخ به کاربر</a>"
    )
    context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="HTML")

    return ConversationHandler.END

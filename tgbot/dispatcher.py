"""
Telegram event handlers
"""

from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot

# 🆕 Import your conversation logic
from tgbot.handlers.onboarding import conversation

# ✅ Define the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", conversation.ask_username)],
    states={
        conversation.ASK_USERNAME: [
            MessageHandler(Filters.text & ~Filters.command, conversation.ask_password)
        ],
        conversation.ASK_PASSWORD: [
            MessageHandler(Filters.text & ~Filters.command, conversation.finish)
        ],
    },
    fallbacks=[],
)

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    # 🧩 Add the new conversation handler
    dp.add_handler(conv_handler)

    # Existing handlers
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    dp.add_handler(
        CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}")
    )

    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'),
                       broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler,
                             pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    dp.add_handler(MessageHandler(Filters.animation, files.show_file_id))
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    return dp

# Bot worker setup
n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))

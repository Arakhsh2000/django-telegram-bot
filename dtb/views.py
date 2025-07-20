import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, Dispatcher
from telegram import Bot

# Your bot token (safe for now, but don't put this on GitHub if public)
TELEGRAM_TOKEN = '7509832280:AAFjevf-fO6bGBC1GK_QDvzN9RCVwV8GPP8'

# Import your handlers and states from your conversation.py
from tgbot.handlers.onboarding.conversation import ask_username, ask_password, finish, ASK_USERNAME, ASK_PASSWORD

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', ask_username)],
    states={
        ASK_USERNAME: [MessageHandler(Filters.text & ~Filters.command, ask_password)],
        ASK_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, finish)],
    },
    fallbacks=[],
)
dispatcher.add_handler(conv_handler)

@method_decorator(csrf_exempt, name='dispatch')
class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        update = Update.de_json(data, bot)
        dispatcher.process_update(update)
        return JsonResponse({"ok": True})

    def get(self, request, *args, **kwargs):
        return JsonResponse({"ok": "Get request received! But nothing done"})

def index(request):
    return JsonResponse({"ok": "Hello! Bot webhook is set up."})

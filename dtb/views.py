import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler

from tgbot.handlers.onboarding.conversation import ask_username, ask_password, finish, ASK_USERNAME, ASK_PASSWORD

# Use your Telegram bot token here
TELEGRAM_TOKEN = '7509832280:AAFjevf-fO6bGBC1GK_QDvzN9RCVwV8GPP8'
bot = Bot(token=TELEGRAM_TOKEN)

# Create dispatcher and handler ONCE, globally
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
        return JsonResponse({"ok": "Webhook endpoint up."})

def index(request):
    return JsonResponse({"ok": "Hello! Bot webhook is set up."})

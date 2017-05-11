from bot.bot_views import StartCommandView, MessageCommandView
from telegrambot.handlers import command, regex

urlpatterns = [
    command('start', StartCommandView.as_command_view()),
    regex(r'(?P<text>\w+)', MessageCommandView.as_command_view()),
]

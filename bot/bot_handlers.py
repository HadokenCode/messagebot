from bot.bot_views import StartCommandView, CloseCommandView, MessageCommandView
from telegrambot.handlers import command, regex

urlpatterns = [
    command('hello', StartCommandView.as_command_view()),
    command('bye', CloseCommandView.as_command_view()),
    regex(r'(?P<text>\w+)', MessageCommandView.as_command_view()),
]

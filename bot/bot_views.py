from telegrambot.bot_views.generic import TemplateCommandView
from bot.models import Message

class StartCommandView(TemplateCommandView):
    template_text = "bot/messages/command_start_text.txt"

class MessageCommandView(TemplateCommandView):
    template_text = "bot/messages/command_write_message_text.txt"
    context_object_name = "response"

    def get_context(self, bot, update, **kwargs):
        user_id = update.message.chat.id
        body = update.message.text
        message = Message(
            user_id = user_id,
            body = body,
            source = Message.SOURCE_TELEGRAM
        )

        message.save()

        context = {self.context_object_name: body }
        return context

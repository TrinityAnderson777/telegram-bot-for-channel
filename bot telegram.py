import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Вставьте сюда токен вашего бота
TOKEN = "вставь свой токен"

# ID чата с модераторами — это группа, где сидят модераторы
# Мы будем брать админов из этого чата и слать им сообщения в ЛС
MODERATION_CHAT_ID = - замени на свой id  # замените на ваш ID группы с модераторами

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь мне любое сообщение, и я предложу подтвердить отправку на модерацию."
    )


async def user_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    keyboard = [
        [InlineKeyboardButton("Отправить на модерацию", callback_data=f"user_confirm")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Вы хотите отправить это сообщение на модерацию?\n\n{text}",
        reply_markup=reply_markup,
    )

    # Сохраняем текст для последующей отправки модераторам
    context.user_data["last_text"] = text


async def send_to_moderators(context: ContextTypes.DEFAULT_TYPE, text: str):
    moderators = []
    async for member in context.bot.get_chat_administrators(MODERATION_CHAT_ID):
        if not member.user.is_bot:
            moderators.append(member.user.id)

    keyboard = [
        [
            InlineKeyboardButton("Одобрить", callback_data=f"approve"),
            InlineKeyboardButton("Отклонить", callback_data=f"reject"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for mod_id in moderators:
        try:
            await context.bot.send_message(
                chat_id=mod_id,
                text=f"Новое сообщение на модерацию:\n\n{text}",
                reply_markup=reply_markup,
            )
        except Exception as e:
            logger.warning(f"Не удалось отправить модератору {mod_id}: {e}")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "user_confirm":
        # Пользователь подтвердил отправку на модерацию
        text = context.user_data.get("last_text")
        if not text:
            await query.edit_message_text("Нет текста для отправки на модерацию.")
            return

        await query.edit_message_text("Сообщение отправлено на модерацию.")

        # Отправляем модераторам в ЛС
        await send_to_moderators(context, text)

    elif data == "approve":
        # Модератор одобрил сообщение
        await query.edit_message_text("Вы одобрили сообщение.")
        # Здесь можно добавить логику публикации сообщения или уведомления

    elif data == "reject":
        # Модератор отклонил сообщение
        await query.edit_message_text("Вы отклонили сообщение.")
        # Здесь можно добавить логику уведомления пользователя

    else:
        await query.edit_message_text(f"Неизвестное действие: {data}")


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(
        # Обрабатываем любые текстовые сообщения от пользователя
        # чтобы предлагать отправить на модерацию
        # если нужно, можно добавить фильтр по чату
        # filters.TEXT & ~filters.COMMAND
        # но в v20 фильтры импортируются из telegram.ext.filters
        # для простоты пропущу фильтр
        # если нужно, добавьте сами
        CommandHandler("dummy", lambda u, c: None)
    )
    application.add_handler(
        # Обработчик сообщений (не команд)
        # Лучше использовать MessageHandler с фильтрами, вот пример:
        # from telegram.ext import MessageHandler, filters
        # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_confirmation))
    )
    from telegram.ext import MessageHandler, filters

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, user_confirmation)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
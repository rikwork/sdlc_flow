import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from .config import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "Welcome to SDLC Flow Bot!\n"
        "I will notify you when a human checkpoint is reached."
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle approval/rejection button clicks."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("approve_"):
        _, task_id, step_id = data.split("_")
        # Logic to mark checkpoint as approved in TaskStore/CheckpointManager
        await query.edit_message_text(text=f"✅ Task {task_id} step {step_id} approved by @{query.from_user.username}")
    elif data.startswith("reject_"):
        _, task_id, step_id = data.split("_")
        # Logic to mark checkpoint as rejected
        await query.edit_message_text(text=f"❌ Task {task_id} step {step_id} rejected by @{query.from_user.username}")


def main() -> None:
    """Start the bot."""
    if not settings.telegram_bot_token:
        print("Telegram bot token not found in settings.")
        return

    application = ApplicationBuilder().token(settings.telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    print("Telegram bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()

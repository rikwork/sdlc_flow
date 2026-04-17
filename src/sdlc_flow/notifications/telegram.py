from typing import Optional
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from ..config import settings


class TelegramNotifier:
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.bot = Bot(token=self.bot_token) if self.bot_token else None

    async def send_message(self, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None) -> None:
        """Send a message to the configured Telegram chat."""
        if not self.bot or not self.chat_id:
            return

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")

    def get_approval_markup(self, task_id: str, step_id: str) -> InlineKeyboardMarkup:
        """Create inline buttons for approval/rejection."""
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{task_id}_{step_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{task_id}_{step_id}")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

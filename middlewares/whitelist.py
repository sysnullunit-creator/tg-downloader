import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Chat, Message, TelegramObject, User

logger = logging.getLogger(__name__)


class WhitelistMiddleware(BaseMiddleware):
    """
    Restricts bot interaction exclusively to pre-approved chat IDs.

    - Whitelisted events are enriched with context flags (`is_admin`, `is_private`, `is_group`).
    - Events from unauthorized chats are dropped silently at the outer middleware layer.
    """

    def __init__(
        self,
        allowed_chat_ids: set[int],
        admin_user_ids: set[int] | None = None,
    ) -> None:
        self.allowed_chat_ids = allowed_chat_ids
        self.admin_user_ids = admin_user_ids or set()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        chat: Chat | None = None
        user: User | None = None

        if isinstance(event, Message):
            chat = event.chat
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            if event.message and isinstance(event.message, Message):
                chat = event.message.chat
            user = event.from_user
        elif hasattr(event, "chat"):
            chat = getattr(event, "chat", None)
            user = getattr(event, "from_user", None)
        elif hasattr(event, "message") and hasattr(event.message, "chat"):
            chat = getattr(event.message, "chat", None)
            user = getattr(event, "from_user", None)

        # If event has no chat associated, allow handler to process normally
        if chat is None:
            return await handler(event, data)

        # Drop unauthorized interactions
        if chat.id not in self.allowed_chat_ids:
            user_id = user.id if user else "unknown"
            username = f"@{user.username}" if (user and user.username) else "no_username"
            chat_title = chat.title or chat.username or "Private Chat"
            logger.warning(
                "Unauthorized access attempt dropped: chat_id=%s ('%s'), from_user=%s (%s)",
                chat.id,
                chat_title,
                user_id,
                username,
            )
            return None

        # Inject permission and context flags for downstream handlers
        is_admin = bool(user and user.id in self.admin_user_ids)
        is_private = chat.id > 0
        is_group = chat.id < 0

        data["is_admin"] = is_admin
        data["is_private"] = is_private
        data["is_group"] = is_group

        return await handler(event, data)

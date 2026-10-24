from unittest.mock import AsyncMock

import pytest
from aiogram.types import CallbackQuery, Chat, Message, User

from config import parse_chat_ids
from middlewares import WhitelistMiddleware


def test_parse_chat_ids_valid():
    raw = "7177930122, 987654321, -1002366722481"
    all_ids, admin_ids, group_ids = parse_chat_ids(raw)

    assert all_ids == {7177930122, 987654321, -1002366722481}
    assert admin_ids == {7177930122, 987654321}
    assert group_ids == {-1002366722481}


def test_parse_chat_ids_empty():
    with pytest.raises(ValueError, match="not found or empty in environment"):
        parse_chat_ids("")

    with pytest.raises(ValueError, match="not found or empty in environment"):
        parse_chat_ids("   ")


def test_parse_chat_ids_invalid_values():
    with pytest.raises(ValueError, match="Invalid chat_id in ALLOWED_CHAT_IDS"):
        parse_chat_ids("123, invalid_id, -100")


@pytest.mark.asyncio
async def test_middleware_authorized_private_message():
    allowed_ids = {7177930122, -1002366722481}
    admin_ids = {7177930122}
    middleware = WhitelistMiddleware(allowed_ids, admin_ids)

    user = User(id=7177930122, is_bot=False, first_name="Admin", username="admin_user")
    chat = Chat(id=7177930122, type="private")
    message = Message(message_id=1, date=None, chat=chat, from_user=user)

    handler = AsyncMock(return_value="handler_executed")
    data = {}

    result = await middleware(handler, message, data)

    assert result == "handler_executed"
    handler.assert_awaited_once_with(message, data)
    assert data["is_admin"] is True
    assert data["is_private"] is True
    assert data["is_group"] is False


@pytest.mark.asyncio
async def test_middleware_authorized_group_message():
    allowed_ids = {7177930122, -1002366722481}
    admin_ids = {7177930122}
    middleware = WhitelistMiddleware(allowed_ids, admin_ids)

    user = User(id=999999, is_bot=False, first_name="RegularMember")
    chat = Chat(id=-1002366722481, type="supergroup", title="Target Group")
    message = Message(message_id=2, date=None, chat=chat, from_user=user)

    handler = AsyncMock(return_value="group_ok")
    data = {}

    result = await middleware(handler, message, data)

    assert result == "group_ok"
    handler.assert_awaited_once_with(message, data)
    assert data["is_admin"] is False
    assert data["is_private"] is False
    assert data["is_group"] is True


@pytest.mark.asyncio
async def test_middleware_unauthorized_message_dropped():
    allowed_ids = {7177930122, -1002366722481}
    middleware = WhitelistMiddleware(allowed_ids)

    unauthorized_chat = Chat(id=999111222, type="private")
    user = User(id=999111222, is_bot=False, first_name="Intruder")
    message = Message(message_id=3, date=None, chat=unauthorized_chat, from_user=user)

    handler = AsyncMock()
    data = {}

    result = await middleware(handler, message, data)

    assert result is None
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_middleware_authorized_callback_query():
    allowed_ids = {7177930122, -1002366722481}
    admin_ids = {7177930122}
    middleware = WhitelistMiddleware(allowed_ids, admin_ids)

    chat = Chat(id=-1002366722481, type="supergroup", title="Target Group")
    message = Message(message_id=4, date=None, chat=chat)
    user = User(id=7177930122, is_bot=False, first_name="Admin")
    callback = CallbackQuery(id="cb1", from_user=user, chat_instance="inst1", message=message)

    handler = AsyncMock(return_value="cb_ok")
    data = {}

    result = await middleware(handler, callback, data)

    assert result == "cb_ok"
    handler.assert_awaited_once_with(callback, data)
    assert data["is_admin"] is True
    assert data["is_group"] is True


@pytest.mark.asyncio
async def test_middleware_unauthorized_callback_query():
    allowed_ids = {7177930122}
    middleware = WhitelistMiddleware(allowed_ids)

    chat = Chat(id=555555, type="private")
    message = Message(message_id=5, date=None, chat=chat)
    user = User(id=555555, is_bot=False, first_name="Stranger")
    callback = CallbackQuery(id="cb2", from_user=user, chat_instance="inst2", message=message)

    handler = AsyncMock()
    data = {}

    result = await middleware(handler, callback, data)

    assert result is None
    handler.assert_not_awaited()

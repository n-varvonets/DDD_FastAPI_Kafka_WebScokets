from datetime import datetime

import pytest

from domain.entities.messages import Message, Chat
from domain.events.messages import NewMessageReceivedEvent
from domain.values.messages import Text, Title
from domain.exceptions.messages import TitleToolLongException


def test_create_message_success_short_text():
    text = Text('hello world')
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text():
    text = Text('a' * 400)
    message = Message(text=text)

    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title('title')
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_title_too_long():
    with pytest.raises(TitleToolLongException):
        Title('title' * 200)


def test_add_chat_to_message():
    text = Text('hello world')
    message = Message(text=text)

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_add_chat_to_events():
    text = Text('hello world')
    message = Message(text=text)

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events
    assert len(events) == 1

    assert message in chat.messages

    new_event = events[0]
    assert isinstance(new_event, NewMessageReceivedEvent)
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.message_oid == message.oid

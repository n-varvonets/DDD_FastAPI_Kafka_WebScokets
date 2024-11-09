from typing import Mapping, Any

from domain.entities.messages import Chat, Message


def convert_message_entity_to_document(message: Message):
    return {
        "oid": message.oid,
        "created_at": message.created_at,
        "text": message.text.as_generic_type(),
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [convert_message_entity_to_document(message) for message in chat.messages],
    }


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        title=chat_document['title'],
        oid=chat_document['oid'],
        created_at=chat_document['created_at'],

        messages=[
            # get messages as entities(not documents)
            convert_message_document_to_entity(message_document)
            for message_document in chat_document['messages']
        ]
    )

def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        text=message_document['text'],
        oid=message_document['oid'],
        created_at=message_document['created_at'],
    )
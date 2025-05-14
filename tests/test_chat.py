from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from langchain_openai import ChatOpenAI

from it_myprompt.settings import Settings


def test_create_chat(client, token, user, mocker):
    mocker.patch(
        'langchain_openai.ChatOpenAI.ainvoke', return_value='Fake response'
    )

    response = client.post(
        '/chat/',
        headers={'Authorization': f'Bearer {token}'},
        json={'prompt': 'Test prompt'},
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    ChatOpenAI.ainvoke.assert_called_once()

    assert data['prompt'] == 'Test prompt'
    assert data['response'] == 'Fake response'
    assert data['user_id'] == str(user.id)
    assert data['model'] == Settings().OPENROUTER_MODEL
    assert datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
    assert isinstance(UUID(data['id']), UUID)


def test_create_chat_exception(client, token, user, mocker):
    mocker.patch(
        'langchain_openai.ChatOpenAI.ainvoke',
        return_value=Exception('Fake exception'),
    )
    response = client.post(
        '/chat/',
        headers={'Authorization': f'Bearer {token}'},
        json={'prompt': 'Test prompt'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

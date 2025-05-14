from http import HTTPStatus
from uuid import UUID


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'name': 'Test',
            'email': 'test@example.com',
            'password': 'password',
        },
    )

    data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert data['name'] == 'Test'
    assert data['email'] == 'test@example.com'
    assert isinstance(UUID(data['id']), UUID)


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'name': 'Test',
            'email': user.email,
            'password': 'password',
        },
    )

    excepted = {'detail': 'Email already exists'}
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == excepted


def test_update_user(client, user, token):
    response = client.put(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test',
            'email': 'update@test.com',
            'password': 'test123',
        },
    )

    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'Test'
    assert data['email'] == 'update@test.com'
    assert data['id'] == str(user.id)


def test_update_user_with_existing_email(client, user, token):
    data = {
        'name': 'John',
        'email': 'john@example.com',
        'password': 'other123',
    }
    client.post('/users/', json=data)

    response = client.put(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Test',
            'email': data.get('email'),
            'password': '123456',
        },
    )

    excepted = {'detail': 'Email already exists'}
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == excepted

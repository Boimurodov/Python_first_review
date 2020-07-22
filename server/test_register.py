import pytest
from werkzeug.security import check_password_hash, generate_password_hash


from server import db
from server.models import User


@pytest.fixture()
def new_user():
    user = User(login='Boimurodov', password=generate_password_hash('222'))
    return user


def test_new_user(new_user):
    assert new_user.login == 'Boimurodov'
    assert check_password_hash(new_user.password, '222')


@pytest.fixture
def register1():
    user = User.query.filter_by(login='boimurodov').first()
    if user:
        return user
    else:
        hash_pwd = generate_password_hash('password1')
        new_user = User(login='boimurodov', password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
    return user


@pytest.fixture
def register2():
    user = User.query.filter_by(login='boimurodov').first()
    if user:
        return user
    else:
        hash_pwd = generate_password_hash('password2')
        new_user = User(login='boimurodov', password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
    return user


def test_register(register1, register2):
    user1 = register1
    user2 = register2
    assert user1.password == user2.password
    assert user1 == user2

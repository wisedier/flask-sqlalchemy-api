from db.models import User


def test_user():
    User.create(name='tester').save(commit=True)

    user = User.get(1)
    assert user is not None and user.name == 'tester'

    user.update(name='tester2', commit=True)
    User.session.close()

    user = User.get(1)
    assert user.name == 'tester2'
    user.delete()
    User.session.close()

    user = User.get(1)
    assert user is None

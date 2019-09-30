from config import config


def test_config():
    assert config.TESTING
    assert 'test' in config.SQLALCHEMY_DATABASE_URI

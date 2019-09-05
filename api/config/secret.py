"""
You have to add this file in `.gitignore` and update `SECRET` value.

Example:
    >>> import binascii
    >>> import os
    >>> binascii.hexlify(os.urandom(32))
"""
SECRET = 'c97b3c67127a885284a9f60f792f53ee35938be4bf1ffe673ef63df67ef7cee1'

db_user = 'api'
db_password = 'api'
db_host = 'localhost'
db_port = 5432
db_name = 'api'
test_db_user = 'test_api'
test_db_password = 'test_api'
test_db_host = 'localhost'
test_db_port = 5432
test_db_name = 'test_api'

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
TEST_SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{test_db_user}:{test_db_password}@{test_db_host}:{test_db_port}/{test_db_name}'
)

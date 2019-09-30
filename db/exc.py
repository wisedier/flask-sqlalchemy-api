from sqlalchemy.exc import SQLAlchemyError


class DBError(SQLAlchemyError):

    def __init__(self, code=None, description=''):
        code = self.__class__.__name__ if not code else code
        super(DBError, self).__init__(description)
        self.description = description
        self.code = code

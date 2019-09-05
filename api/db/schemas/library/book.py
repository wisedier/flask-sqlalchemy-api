import marshmallow as mm

from db.schemas.library.author import AuthorSchema


class BookSchema(mm.Schema):
    id = mm.fields.Int()
    name = mm.fields.Str()
    author = mm.fields.Nested(AuthorSchema)
    edition = mm.fields.Int()

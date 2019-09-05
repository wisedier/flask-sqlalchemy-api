import marshmallow as mm


class AuthorSchema(mm.Schema):
    id = mm.fields.Int()
    name = mm.fields.Str()

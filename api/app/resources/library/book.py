from flask_restful import reqparse

from api.app import status
from api.app.ext import api
from api.app.resources import APIResource
from db.models import Book
from db.schemas import BookSchema


class BookAPI(APIResource):

    def get(self):
        """
        Get books
        ---
        tags:
          - Library
        description:
        parameters:
          - in: query
            name: page
            schema:
              type: integer
              minimum: 1
            description: page number
            required: false
          - in: query
            name: per_page
            schema:
              type: integer
              minimum: 5
            description: the number of books to retrieve per each page
            required: false
        responses:
          200:
            description: Book list
            schema:
              $ref: '#/definitions/Book'
        """
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args', default=1, required=False)
        parser.add_argument('per_page', type=int, location='args', default=10, required=False)
        args = parser.parse_args()

        page = self.get_page(args)
        per_page = self.get_per_page(args)
        books = Book.query.paginate(page, per_page, BookSchema(many=True)).to_dict()
        return books, status.HTTP_200_OK


api.add_resource(
    BookAPI,
    '/books/',
    endpoint='books',
)

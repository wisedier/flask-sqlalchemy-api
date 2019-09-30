import collections
from math import ceil

import marshmallow


class Pagination(object):
    """
    Modified version of Pagination class from [1]
    [1]: https://github.com/pallets/flask-sqlalchemy/blob/master/flask_sqlalchemy/__init__.py
    """

    def __init__(self, query, page, per_page, total, items, item_schema: marshmallow.Schema):
        self.query = query
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        self.item_schema = item_schema

    @property
    def pages(self):
        pages = 0
        if self.per_page != 0 and self.total is not None:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self, error_out=False):
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if (num <= left_edge or
                (self.page - left_current - 1 < num < self.page + right_current) or
                num > self.pages - right_edge):
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def to_dict(self):
        items = []
        if self.item_schema is not None:
            items = self.item_schema.dump(self.items)

        return collections.OrderedDict(
            page=self.page,
            pages=self.pages,
            has_prev=self.has_prev,
            has_next=self.has_next,
            total_count=self.total,
            items_per_page=self.per_page,
            items=items
        )

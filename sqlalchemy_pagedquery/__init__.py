import math

from sqlalchemy.orm import Query


class PagedQueryResult(object):

    def __init__(self, objects, page, per_page, total_records):
        self.objects = objects
        self.page = page
        self.per_page = per_page
        self.total_records = total_records

    def params(self):
        """Return the non-object parameters of this collection as a dict"""
        return {'page': self.page,
                'per_page': self.per_page,
                'total_records': self.total_records}

    def __repr__(self):
        return '<PagedQueryResult ({} records of {} total)>'.format(len(self.objects), self.total_records)


class PagedQuery(Query):

    def all_paged(self, page, per_page):
        """Same as Query.all(), but return a PagedQueryResult wrapping the resultset with attributes
        to help paging"""

        # Coerce arguments to float
        page = float(page)
        per_page = float(per_page)

        total_records = self.count()
        offset = per_page * (page - 1)
        query = self.limit(per_page).offset(offset)

        objects = query.all()

        return PagedQueryResult(objects, page, per_page, total_records)
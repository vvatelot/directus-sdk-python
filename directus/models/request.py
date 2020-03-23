# -*- coding: utf-8 -*-

from typing import List, Optional

from ..typing import RequestFields

# pylint: disable=too-few-public-methods


class ListParameters:
    "Common List parameters object"

    def __init__(
        self,
        status: Optional[str] = None,
        single: bool = False,
        fields: Optional[RequestFields] = None,
        sort: Optional[List[str]] = None,
        list_filter: Optional[str] = None,
        query: Optional[str] = None,
    ) -> None:
        self.status = status
        self.single = single
        self.fields = ",".join(fields or ["*"])
        self.sort = ",".join(sort or ["id"])
        self.filter = list_filter
        # pylint: disable=invalid-name
        self.q = query


class ListPagination:
    "Common Pagination object"

    def __init__(
        self, page: Optional[int] = None, limit: int = 100, offset: int = 0
    ) -> None:
        if page:
            self.page = page
        else:
            self.limit = limit
            self.offset = offset

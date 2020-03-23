# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

from ..typing import Item, RequestMeta, ResponseMeta, Revision
from ..utils import ApiClient
from ..models import ListParameters, ListPagination


class ItemsMixin:
    """

    Items
    https://docs.directus.io/api/items.html

    """

    api_client: ApiClient
    page_recursive_get_all: int = 0

    def get_items_list(
        self,
        collection: str,
        parameters: Optional[ListParameters] = None,
        pagination: Optional[ListPagination] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[List[Item], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#list-the-items

        If page is set, offset is not taken into account

        If single, only return first corresponding result from list

        Returns
        -------
            (List of Item, Metadata)
        """

        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="/".join(["items", collection]),
            params={
                **vars(pagination or ListPagination()),
                **vars(parameters or ListParameters()),
            },
            meta=meta or [],
        )

        return list(response_data), response_meta

    def get_all_items_list(
        self,
        collection: str,
        parameters: Optional[ListParameters] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[List[Item], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#list-the-items

        Returns
        -------
            (List of Item, Metadata)
        """
        meta = meta or []
        if "page" not in meta:
            meta.append("page")

        response_data, response_meta = self.get_items_list(
            collection=collection,
            pagination=ListPagination(page=self.page_recursive_get_all + 1),
            parameters=parameters,
            meta=meta,
        )

        if int(response_meta["page"]) < int(response_meta["page_count"]):
            recursive_data, _ = self.get_all_items_list(
                collection=collection, parameters=parameters, meta=meta,
            )

            response_data += recursive_data

        return response_data, response_meta

    def get_item(
        self, collection: str, item_id: int, meta: Optional[RequestMeta] = None,
    ) -> Tuple[Item, ResponseMeta]:
        """

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="GET",
            path="/".join(["items", collection, str(item_id)]),
            meta=meta or [],
        )

    def create_item(
        self, collection: str, item_data: Item, meta: Optional[RequestMeta] = None
    ) -> Tuple[Item, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#create-an-item

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="POST",
            path="/".join(["items", collection]),
            data=item_data,
            meta=meta or [],
        )

    def update_item(
        self,
        collection: str,
        item_id: int,
        item_data: dict,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Item, ResponseMeta]:
        """

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="PATCH",
            path="/".join(["items", collection, str(item_id)]),
            data=item_data,
            meta=meta or [],
        )

        """
        Find out more: https://docs.directus.io/api/items.html#delete-an-item

        Returns
        -------
            bool (True if deleted, False if not)
        """

        return self.api_client.make_request(
            method="DELETE", path="/".join(["items", collection, str(item_id)])
        )

    def get_item_revisions_list(
        self,
        collection: str,
        item_id: int,
        limit: int = 100,
        offset: int = 0,
        page: Optional[int] = None,
        single: bool = False,
        item_filter: Optional[dict] = None,
        query: Optional[str] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[List[Revision], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#list-item-revisions

        If page is set, offset is not taken into account

        If single, only return first corresponding result from list

        Returns
        -------
            (List of revision, Metadata)
        """

        params = {
            "limit": limit,
            "offset": offset,
            "sort": ",".join(sort or ["id"]),
            "filter": item_filter or {},
            "q": query,
        }

        if page:
            params["page"] = page
            del params["offset"]

        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="/".join(["items", collection, str(item_id), "revisions"]),
            params=params,
            meta=meta or [],
        )

        return list(response_data), response_meta

    def get_item_revision(
        self,
        collection: str,
        item_id: int,
        offset: int,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Revision, ResponseMeta]:
        """

        Returns
        -------
            (revision, Metadata)
        """

        return self.api_client.make_request(
            method="GET",
            path="/".join(
                ["items", collection, str(item_id), "revisions", str(offset)]
            ),
            meta=meta or [],
        )

    def update_item(
        self,
        collection: str,
        item_id: int,
        revision_id: int,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Revision, ResponseMeta]:
        """

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="PATCH",
            path="/".join(
                ["items", collection, str(item_id), "revert", str(revision_id)]
            ),
            meta=meta or [],
        )

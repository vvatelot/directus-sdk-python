# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

from ..typing import Item, RequestFields, RequestMeta, ResponseMeta, Revision
from ..utils import ApiClient


class ItemsMixin:
    """

    Items
    https://docs.directus.io/api/items.html

    """

    api_client: ApiClient

    def get_items_list(
        self,
        collection: str,
        fields: Optional[RequestFields] = None,
        page: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        sort: Optional[List[str]] = None,
        single: bool = False,
        item_filter: Optional[dict] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
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

        params = {
            "fields": ",".join(fields or ["*"]),
            "limit": limit,
            "offset": offset,
            "sort": ",".join(sort or ["id"]),
            "single": single,
            "filter": item_filter,
            "status": status,
            "q": query,
        }

        if page:
            params["page"] = page
            del params["offset"]

        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="/".join(["items", collection]),
            params=params,
            meta=meta or [],
        )

        return list(response_data), response_meta

    def get_all_items_list(
        self,
        collection: str,
        fields: Optional[RequestFields] = None,
        sort: Optional[List[str]] = None,
        item_filter: Optional[dict] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        meta: Optional[RequestMeta] = None,
        page: int = 1,
    ) -> Tuple[List[Item], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#list-the-items

        Returns
        -------
            (List of Item, Metadata)
        """
        meta = meta if meta else []
        if "page" not in meta:
            meta.append("page")

        response_data, response_meta = self.get_items_list(
            collection=collection,
            fields=fields or ["*"],
            sort=sort or ["id"],
            item_filter=item_filter or {},
            page=page,
            status=status,
            query=query,
            meta=meta,
        )

        if int(response_meta["page"]) < int(response_meta["page_count"]):
            next_page = int(response_meta["page"]) + 1
            recursive_data, _ = self.get_all_items_list(
                collection=collection,
                fields=fields,
                page=next_page,
                sort=sort,
                item_filter=item_filter,
                status=status,
                query=query,
                meta=meta,
            )

            response_data += recursive_data

        return response_data, response_meta

    def get_item(
        self,
        collection: str,
        item_id: int,
        fields: Optional[RequestFields] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Item, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#retrieve-an-item

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="GET",
            path="/".join(["items", collection, str(item_id)]),
            params={"fields": ",".join(fields or ["*"])},
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
        fields: Optional[RequestFields] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Item, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#update-an-item

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="PATCH",
            path="/".join(["items", collection, str(item_id)]),
            data=item_data,
            params={"fields": fields or ["*"]},
            meta=meta or [],
        )

    def delete_item(self, collection: str, item_id: int) -> Tuple[dict, ResponseMeta]:
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
        fields: Optional[RequestFields] = None,
        limit: int = 100,
        offset: int = 0,
        page: Optional[int] = None,
        sort: Optional[List[str]] = None,
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
            "fields": ",".join(fields or ["*"]),
            "limit": limit,
            "offset": offset,
            "sort": ",".join(sort or ["id"]),
            "single": single,
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
        fields: Optional[RequestFields] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Revision, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#retrieve-an-item-revision

        Returns
        -------
            (revision, Metadata)
        """

        return self.api_client.make_request(
            method="GET",
            path="/".join(
                ["items", collection, str(item_id), "revisions", str(offset)]
            ),
            params={"fields": ",".join(fields or ["*"])},
            meta=meta or [],
        )

    def revert_item_revision(
        self,
        collection: str,
        item_id: int,
        revision_id: int,
        fields: Optional[RequestFields] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[Revision, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/items.html#revert-to-a-given-revision

        Returns
        -------
            (Item, Metadata)
        """

        return self.api_client.make_request(
            method="PATCH",
            path="/".join(
                ["items", collection, str(item_id), "revert", str(revision_id)]
            ),
            params={"fields": ",".join(fields or ["*"])},
            meta=meta or [],
        )

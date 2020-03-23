# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

from ..typing import Collection, RequestMeta, ResponseMeta
from ..utils import ApiClient


class CollectionsMixin:
    """

    Collections
    https://docs.directus.io/api/collections.html

    """

    api_client: ApiClient

    def get_collections_list(
        self, offset: int = 0, single: bool = False, meta: Optional[RequestMeta] = None
    ) -> Tuple[List[Collection], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/collections.html#list-collections

        Returns
        -------
            (List of Collection, Metadata)
        """

        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="collections",
            params={"offset": offset, "single": int(single)},
            meta=meta or [],
        )

        return list(response_data), response_meta

    def get_collection(
        self, collection: str, meta: Optional[RequestMeta] = None
    ) -> Tuple[Collection, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/collections.html#retrieve-a-collection

        Returns
        -------
            (Collection, Metadata)
        """

        return self.api_client.make_request(
            method="GET", path="/".join(["collections", collection]), meta=meta or [],
        )

    def create_collection(
        self, collection: Collection, meta: Optional[RequestMeta] = None
    ) -> Tuple[Collection, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/collections.html#create-a-collection

        Returns
        -------
            (Collection, Metadata)
        """

        return self.api_client.make_request(
            method="POST", path="collections", data=collection, meta=meta or [],
        )

    def update_collection(
        self, collection: str, data: dict, meta: Optional[RequestMeta] = None
    ) -> Tuple[Collection, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/collections.html#update-a-collection

        Returns
        -------
            (Collection, Metadata)
        """

        return self.api_client.make_request(
            method="PATCH",
            path=f"collections/{collection}",
            data=data,
            meta=meta or [],
        )

    def delete_collection(self, collection: str) -> Tuple[Collection, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/collections.html#delete-a-collection

        Returns
        -------
            bool (True if deleted, False if not)
        """
        path = f"collections/{collection}"

        return self.api_client.make_request(method="DELETE", path=path)

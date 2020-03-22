# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

from .exceptions import DirectusException
from .utils import ApiClient
from .typing import (
    RequestMeta,
    RequestFields,
    ResponseMeta,
    Collection,
    Item,
    Revision,
    File,
)


class DirectusClient:
    """
    DirectusClient provide a way to interact with Directus API on a defined server.
    It eases the use of [Directus API](https://docs.directus.io/api/reference.html) by providing
    simple methods to access to the resources.

    Attributes
    ----------
    url: str
        The url of the Directus server you want to connect to

    email: str
        The email account you want to use to connect to the Directus server

    password: str
        The associated password corresponding to the email account

    project: str
        The name of the project you want to access on the specified server
    """

    def __init__(
        self,
        url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        project: Optional[str] = None,
    ):
        if not url:
            raise DirectusException("You must provide a server url")

        if not project:
            raise DirectusException("You must provide a project")

        if not email and password:
            raise DirectusException("You must provide an email")

        if not password and email:
            raise DirectusException("You must provide a password")

        self.api_client = ApiClient(
            url=url, email=email, password=password, project=project
        )

    """

    Collections
    https://docs.directus.io/api/collections.html

    """

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

    """

    Items
    https://docs.directus.io/api/items.html

    """

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

    """

    Files
    https://docs.directus.io/api/files.html

    """

    def get_files_list(
        self,
        fields: Optional[RequestFields] = None,
        limit: int = 100,
        offset: int = 0,
        sort: Optional[List[str]] = None,
        single: bool = False,
        file_filter: Optional[dict] = None,
        status: Optional[str] = None,
        query: Optional[str] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[List[File], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/files.html#list-the-files

        If single, only return first corresponding result from list

        Returns
        -------
            (List of File, Metadata)
        """

        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="files",
            params={
                "fields": ",".join(fields or ["*"]),
                "limit": limit,
                "offset": offset,
                "sort": ",".join(sort or ["id"]),
                "single": single,
                "filter": file_filter or {},
                "status": status,
                "q": query,
            },
            meta=meta or [],
        )

        return list(response_data), response_meta

    def get_file(
        self,
        file_id: int,
        fields: Optional[RequestFields] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[File, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/files.html#retrieve-a-file

        Returns
        -------
            (File, Metadata)
        """

        return self.api_client.make_request(
            method="GET",
            path="/".join(["files", str(file_id)]),
            params={"fields": ",".join(fields or ["*"])},
            meta=meta or [],
        )

    def create_file(
        self,
        data: str,
        filename_download: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[str] = None,
        metadata: Optional[str] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[File, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/files.html#create-a-file

        Returns
        -------
            (File, Metadata)
        """

        params = {"data": data}

        if filename_download:
            params["filename_downlad"] = filename_download
        if title:
            params["title"] = title
        if description:
            params["description"] = description
        if location:
            params["location"] = location
        if tags:
            params["tags"] = tags
        if metadata:
            params["metadata"] = metadata

        return self.api_client.make_request(
            method="POST", path="files", data=params, meta=meta or []
        )

    """

    Mail
    https://docs.directus.io/api/mail.html

    """

    def send_email(
        self,
        send_to: List[str],
        subject: str,
        body: str,
        body_type: Optional[str] = "txt",
        data: Optional[dict] = None,
    ) -> Tuple[dict, ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/mail.html#send-an-email

        Returns
        -------
            (Empty body, Metadata)
        """

        return self.api_client.make_request(
            method="POST",
            path="mail",
            data={
                "to": send_to,
                "subject": subject,
                "body": body,
                "type": body_type,
                "data": data or {},
            },
        )

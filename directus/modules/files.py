# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple

from ..typing import File, RequestFields, RequestMeta, ResponseMeta
from ..utils import ApiClient


class FilesMixin:
    """

    Files
    https://docs.directus.io/api/files.html

    """

    api_client: ApiClient

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

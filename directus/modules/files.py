# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple, Callable

from ..typing import File, RequestFields, RequestMeta, ResponseMeta
from ..utils import ApiClient
from ..models import ListPagination, ListParameters


class FilesMixin:
    """

    Files
    https://docs.directus.io/api/files.html

    """

    api_client: ApiClient
    generate_parameters: Callable

    def get_files_list(
        self,
        parameters: Optional[ListParameters] = None,
        pagination: Optional[ListPagination] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[List[File], ResponseMeta]:
        """
        Find out more: https://docs.directus.io/api/files.html#list-the-files


        Returns
        -------
            (List of File, Metadata)
        """
        response_data, response_meta = self.api_client.make_request(
            method="GET",
            path="files",
            params=self.generate_parameters(
                parameters=parameters, pagination=pagination
            ),
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

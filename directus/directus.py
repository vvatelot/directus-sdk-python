# -*- coding: utf-8 -*-

from typing import Optional

from .exceptions import DirectusException
from .modules import CollectionsMixin, FilesMixin, ItemsMixin
from .utils import ApiClient
from .models import ListPagination, ListParameters


class DirectusClient(CollectionsMixin, ItemsMixin, FilesMixin):
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

    @staticmethod
    def generate_parameters(
        parameters: Optional[ListParameters], pagination: Optional[ListPagination]
    ) -> dict:
        "Generate requests parameters from directus parameters and pagination"
        return {
            **vars(pagination or ListPagination()),
            **vars(parameters or ListParameters()),
        }

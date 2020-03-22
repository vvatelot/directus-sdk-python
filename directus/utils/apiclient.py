# -*- coding: utf-8 -*-

from json.decoder import JSONDecodeError
from time import time
from typing import Optional, Tuple
from urllib.parse import urljoin
from http import HTTPStatus

from jwt import decode
from requests import request

from ..exceptions import DirectusException
from ..typing import (
    RequestData,
    RequestHeaders,
    RequestMeta,
    RequestParams,
    ResponseMeta,
)


class ApiClient:  # pylint: disable=too-few-public-methods
    """
    This class make the connection to the Directus API. It implements
    existing REST methods described in the documentation:
    https://docs.directus.io/api/reference.html
    """

    def __init__(
        self,
        url: str,
        project: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.base_header = {}
        self.token = ""
        self.url = url
        self.base_url = urljoin(base=url, url=project)
        self.project = project
        if email and password:
            auth, _ = self.make_request(
                method="POST",
                path="auth/authenticate",
                data={"email": email, "password": password},
            )
            self.token = auth["token"]
            self.base_header["authorization"] = f"Bearer {self.token}"

    def make_request(
        self,
        method: str,
        path: str,
        data: Optional[RequestData] = None,
        params: Optional[RequestParams] = None,
        headers: Optional[RequestHeaders] = None,
        meta: Optional[RequestMeta] = None,
    ) -> Tuple[dict, ResponseMeta]:
        "Generic REST request method"

        if method not in ["GET", "POST", "PATCH", "DELETE"]:
            raise DirectusException(
                f"Method {method} not allowed. Only metods GET, POST, PATCH and DELETE"
            )

        self.auto_refresh_token()

        response = request(
            method=method,
            url=self.set_url(path=path),
            headers=self.set_headers(headers=headers),
            json=data,
            params=self.set_params(params=params, meta=meta),
        )

        try:
            if response.json().get("error"):
                raise DirectusException(
                    (
                        f"{response.json()['error']['message']}"
                        f"( Code {response.json()['error']['code']}: "
                        f"Please have a look at https://docs.directus.io/api/errors.html )"
                    )
                )

            result = response.json()

            if method in ["GET", "POST", "PATCH"]:
                return result["data"], result.get("meta") or {}

            if method == "DELETE":
                if not response:
                    raise DirectusException("DELETE Operation went wrong")

                if response.status_code != HTTPStatus.NO_CONTENT:
                    raise DirectusException(
                        "DELETE Operation went wrong. "
                        f"Response status code is: {response.status_code}"
                    )

                return {}, {}

        except JSONDecodeError:
            return {}, {}

        return {}, {}

    def auto_refresh_token(self) -> None:
        "Call refresh token API to update JWT token"
        if self.token:
            decoded_token = decode(self.token, verify=False)

        if self.token and int(decoded_token["exp"] - 60) < int(time()):
            new_token, _ = self.make_request(
                method="POST",
                path="/".join(["auth", "refresh"]),
                data={"token": self.token},
            )
            self.token = new_token["token"]
            self.base_header["token"] = new_token["token"]

    @staticmethod
    def set_params(
        params: Optional[RequestParams], meta: Optional[RequestMeta]
    ) -> RequestParams:
        "Generate request params"
        params = params or {}
        if meta:
            params["meta"] = ",".join(meta)

        return params

    def set_headers(self, headers: Optional[RequestHeaders]) -> RequestHeaders:
        "Generate request headers"
        return {**self.base_header, **headers} if headers else self.base_header

    def set_url(self, path: str) -> str:
        "Generate url based on base url and path"
        return "/".join([self.base_url, path])

import requests
from aws_lambda_powertools.utilities import parameters
import os
import json
from jsonschema import validate
from typing import Tuple
from boto3 import Session


schema = {
    "type": "object",
    "properties": {
        "API_KEY": {"type": "string"},
        "API_ENDPOINT_URL": {"type": "string"},
    },
    "required": ["API_KEY", "API_ENDPOINT_URL"],
}


class CrossAccountClientContextManager(object):
    def __init__(self, service_name, role_arn, role_session_name, **kwargs):
        super().__init__()
        self.service_name = service_name
        self.role_arn = role_arn
        self.role_session_name = role_session_name
        self.kwargs = kwargs

    def __enter__(self):
        sts = Session().client("sts")
        if "external_id" in self.kwargs:
            assumed_role_object = sts.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName=self.role_session_name,
                ExternalId=self.kwargs["external_id"],
            )
        else:
            assumed_role_object = sts.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName=self.role_session_name,
            )
        self.credentials = assumed_role_object["Credentials"]
        kwargs = {
            "service_name": self.service_name,
            "aws_access_key_id": self.credentials["AccessKeyId"],
            "aws_secret_access_key": self.credentials["SecretAccessKey"],
            "aws_session_token": self.credentials["SessionToken"],
        }
        if self.kwargs is not None:
            kwargs.update(self.kwargs)
            del kwargs["external_id"]
        self.client = Session().client(**kwargs)
        return self.client

    def __exit__(self, *args, **kwargs):
        self.client = None


class BearerAuthSecretsManager(requests.auth.AuthBase):
    def __init__(self):
        if "SECRET_NAME" not in os.environ:
            raise EnvironmentError("Lambda is missing ENV variable SECRET_NAME!")
        else:
            secret_name = os.getenv("SECRET_NAME")
        self.__secret = json.loads(parameters.get_secret(secret_name))
        validate(instance=self.__secret, schema=schema)
        self.__security_token = self.__secret.get("API_KEY")
        self.__api_endpoint_url = self.__secret.get("API_ENDPOINT_URL")
        self.__jwt_token, _ = self.create_session_bearer_token()

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer {}".format(self.__jwt_token)
        r.headers["Accept"] = "application/json"
        return r

    def create_session_bearer_token(self) -> Tuple[str, str]:
        headers = {"Accept": "application/json"}
        payload = {"security_token": self.__security_token}
        r = requests.post(
            "{}/user/session".format(self.__api_endpoint_url),
            data=payload,
            headers=headers,
        )
        r.raise_for_status()
        response_json = r.json()
        if "jwt" not in response_json:
            raise KeyError("JWT key not found in Orca response!")

        return response_json["jwt"]["access"], response_json["jwt"]["refresh"]

    @property
    def token(self):
        return self.__security_token

    @property
    def api_endpoint_url(self):
        return self.__api_endpoint_url

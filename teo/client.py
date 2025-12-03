import json

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.teo.v20220901 import models, teo_client

from logger.logger import get_logger
from setting import REGION, SECRET_ID, SECRET_KEY

logger = get_logger(__name__)


class TEOClient:
    def __init__(self):
        self._client = teo_client.TeoClient(
            credential=credential.Credential(secret_id=SECRET_ID, secret_key=SECRET_KEY), region=REGION, profile=None
        )

    def describe_origin_acl(self, zone_id: str) -> models.DescribeOriginACLResponse:
        try:
            req = models.DescribeOriginACLRequest()
            req.from_json_string(json.dumps({"ZoneId": zone_id}))
            return self._client.DescribeOriginACL(req)
        except TencentCloudSDKException as err:
            logger.error("[TEOClient] DescribeOriginACL error: %s", err)
            raise err

    def confirm_origin_acl_update(self, zone_id: str) -> models.ConfirmOriginACLUpdateResponse:
        try:
            req = models.ConfirmOriginACLUpdateRequest()
            req.from_json_string(json.dumps({"ZoneId": zone_id}))
            return self._client.ConfirmOriginACLUpdate(req)
        except TencentCloudSDKException as err:
            logger.error("[TEOClient] ConfirmOriginACLUpdate error: %s", err)
            raise err

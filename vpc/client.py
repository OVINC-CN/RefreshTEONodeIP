import json
from typing import List

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.vpc.v20170312 import models, vpc_client

from logger.logger import get_logger
from setting import (
    REGION,
    SECRET_ID,
    SECRET_KEY,
    SECURITY_GROUP_PORT,
    SECURITY_GROUP_PROTOCOL,
)

logger = get_logger(__name__)


class VPCClient:
    def __init__(self):
        self._client = vpc_client.VpcClient(
            credential=credential.Credential(secret_id=SECRET_ID, secret_key=SECRET_KEY), region=REGION, profile=None
        )

    def describe_address_templates(self, offset: int, limit: int) -> models.DescribeAddressTemplatesResponse:
        try:
            req = models.DescribeAddressTemplatesRequest()
            req.from_json_string(json.dumps({"Offset": str(offset), "Limit": str(limit)}))
            return self._client.DescribeAddressTemplates(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] DescribeAddressTemplates error: %s", err)
            raise err

    def create_address_template(self, name: str, addresses: List[str]) -> models.CreateAddressTemplateResponse:
        try:
            req = models.CreateAddressTemplateRequest()
            req.from_json_string(json.dumps({"AddressTemplateName": name, "Addresses": addresses}))
            return self._client.CreateAddressTemplate(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] CreateAddressTemplate error: %s", err)
            raise err

    def delete_address_template(self, tmpl_id: str) -> models.DeleteAddressTemplateResponse:
        try:
            req = models.DeleteAddressTemplateRequest()
            req.from_json_string(json.dumps({"AddressTemplateId": tmpl_id}))
            return self._client.DeleteAddressTemplate(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] DeleteAddressTemplate error: %s", err)
            raise err

    def describe_address_template_groups(self, offset: int, limit: int) -> models.DescribeAddressTemplateGroupsResponse:
        try:
            req = models.DescribeAddressTemplateGroupsRequest()
            req.from_json_string(json.dumps({"Offset": str(offset), "Limit": str(limit)}))
            return self._client.DescribeAddressTemplateGroups(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] DescribeAddressTemplateGroups error: %s", err)
            raise err

    def create_address_template_group(
        self, name: str, tmpl_ids: List[str]
    ) -> models.CreateAddressTemplateGroupResponse:
        try:
            req = models.CreateAddressTemplateGroupRequest()
            req.from_json_string(json.dumps({"AddressTemplateGroupName": name, "AddressTemplateIds": tmpl_ids}))
            return self._client.CreateAddressTemplateGroup(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] CreateAddressTemplateGroup error: %s", err)
            raise err

    def delete_address_template_group(self, group_id: str) -> models.DeleteAddressTemplateGroupResponse:
        try:
            req = models.DeleteAddressTemplateGroupRequest()
            req.from_json_string(json.dumps({"AddressTemplateGroupId": group_id}))
            return self._client.DeleteAddressTemplateGroup(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] DeleteAddressTemplateGroup error: %s", err)
            raise err

    def describe_security_group_policies(self, security_group_id: str) -> models.DescribeSecurityGroupPoliciesResponse:
        try:
            req = models.DescribeSecurityGroupPoliciesRequest()
            req.from_json_string(json.dumps({"SecurityGroupId": security_group_id}))
            return self._client.DescribeSecurityGroupPolicies(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] DescribeSecurityGroupPolicies error: %s", err)
            raise err

    def replace_security_group_policy(
        self, security_group_id: str, policy_index: int, group_id: str, note: str
    ) -> models.ReplaceSecurityGroupPolicyResponse:
        try:
            req = models.ReplaceSecurityGroupPolicyRequest()
            req.from_json_string(
                json.dumps(
                    {
                        "SecurityGroupId": security_group_id,
                        "SecurityGroupPolicySet": {
                            "Ingress": [
                                {
                                    "PolicyIndex": policy_index,
                                    "Protocol": SECURITY_GROUP_PROTOCOL,
                                    "Port": SECURITY_GROUP_PORT,
                                    "AddressTemplate": {"AddressGroupId": group_id},
                                    "Action": "ACCEPT",
                                    "PolicyDescription": note,
                                }
                            ],
                        },
                    }
                )
            )
            return self._client.ReplaceSecurityGroupPolicy(req)
        except TencentCloudSDKException as err:
            logger.error("[VPCClient] ReplaceSecurityGroupPolicy error: %s", err)
            raise err

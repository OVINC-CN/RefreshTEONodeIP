import datetime

from logger.logger import get_logger
from setting import (
    ADDRESS_TEMPLATE_GROUP_NAME,
    ADDRESS_TEMPLATE_GROUP_PREFIX,
    ADDRESS_TEMPLATE_MAX_ITEMS,
    ADDRESS_TEMPLATE_NAME,
    ADDRESS_TEMPLATE_PREFIX,
    QUERY_LIMIT,
    SECURITY_GROUP_ID,
    SECURITY_GROUP_NOTE,
    SECURITY_GROUP_NOTE_PREFIX,
    ZONE_IDS,
)
from teo.client import TEOClient
from vpc.client import VPCClient

logger = get_logger(__name__)


# pylint: disable=R0914,R0912
def do():
    # task name
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # init client
    teo_client = TEOClient()
    vpc_client = VPCClient()

    # query node ips
    acl_updated = False
    ipv4_set = set()
    ipv6_set = set()
    for zone_id in ZONE_IDS:
        acl_response = teo_client.describe_origin_acl(zone_id=zone_id)
        ipv4_set |= set(acl_response.OriginACLInfo.CurrentOriginACL.EntireAddresses.IPv4)
        ipv6_set |= set(acl_response.OriginACLInfo.CurrentOriginACL.EntireAddresses.IPv6)
        if acl_response.OriginACLInfo.NextOriginACL:
            ipv4_set |= set(acl_response.OriginACLInfo.NextOriginACL.EntireAddresses.IPv4)
            ipv6_set |= set(acl_response.OriginACLInfo.NextOriginACL.EntireAddresses.IPv6)
            acl_updated = True
        logger.info(
            "[RefreshOriginACL] ZoneId: %s, IPv4 count: %d, IPv6 count: %d", zone_id, len(ipv4_set), len(ipv6_set)
        )

    # convert to list
    ip_list = list(ipv4_set | ipv6_set)
    ip_list.sort()

    # bind ip to address template
    tmpl_ids = []
    for i in range(0, len(ip_list), ADDRESS_TEMPLATE_MAX_ITEMS):
        end = min(len(ip_list), i + ADDRESS_TEMPLATE_MAX_ITEMS)
        tmpl_ids.append(
            vpc_client.create_address_template(
                name=ADDRESS_TEMPLATE_NAME.format(date=date, index=i // ADDRESS_TEMPLATE_MAX_ITEMS),
                addresses=ip_list[i:end],
            ).AddressTemplate.AddressTemplateId
        )
    logger.info("[RefreshOriginACL] Created %d address templates", len(tmpl_ids))

    # bind address template to address group
    group_id = vpc_client.create_address_template_group(
        name=ADDRESS_TEMPLATE_GROUP_NAME.format(date=date), tmpl_ids=tmpl_ids
    ).AddressTemplateGroup.AddressTemplateGroupId
    logger.info("[RefreshOriginACL] Created address template group: %s", group_id)

    # bind security group policy
    old_ingress = vpc_client.describe_security_group_policies(
        security_group_id=SECURITY_GROUP_ID
    ).SecurityGroupPolicySet.Ingress
    to_replace_policy_indexes = -1
    for i in old_ingress:
        if i.PolicyDescription.startswith(SECURITY_GROUP_NOTE_PREFIX):
            to_replace_policy_indexes = i.PolicyIndex
            break
    vpc_client.replace_security_group_policy(
        SECURITY_GROUP_ID, to_replace_policy_indexes, group_id, SECURITY_GROUP_NOTE.format(date=date)
    )
    logger.info("[RefreshOriginACL] Replaced security group policy at index: %d", to_replace_policy_indexes)

    # confirm acl update if needed
    if acl_updated:
        for zone_id in ZONE_IDS:
            teo_client.confirm_origin_acl_update(zone_id=zone_id)
        logger.info("[RefreshOriginACL] Confirmed Origin ACL update for all zones")

    # remove old address group
    total = vpc_client.describe_address_template_groups(0, 1).TotalCount
    for i in range(0, total, QUERY_LIMIT):
        for g in vpc_client.describe_address_template_groups(offset=i, limit=QUERY_LIMIT).AddressTemplateGroupSet:
            if g.AddressTemplateGroupId != group_id and g.AddressTemplateGroupName.startswith(
                ADDRESS_TEMPLATE_GROUP_PREFIX
            ):
                vpc_client.delete_address_template_group(group_id=g.AddressTemplateGroupId)
                logger.info("[RefreshOriginACL] Removed old address template group: %s", g.AddressTemplateGroupId)

    # remove old address template
    total = vpc_client.describe_address_templates(0, 1).TotalCount
    for i in range(0, total, QUERY_LIMIT):
        for t in vpc_client.describe_address_templates(offset=i, limit=QUERY_LIMIT).AddressTemplateSet:
            if t.AddressTemplateId not in tmpl_ids and t.AddressTemplateName.startswith(ADDRESS_TEMPLATE_PREFIX):
                vpc_client.delete_address_template(tmpl_id=t.AddressTemplateId)
                logger.info("[RefreshOriginACL] Removed old address template: %s", t.AddressTemplateId)


if __name__ == "__main__":
    do()

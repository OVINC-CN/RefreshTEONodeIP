# Refresh TEO Node IP

This tool automatically refreshes Tencent Cloud TEO (EdgeOne) node IPs in a VPC Security Group. It fetches the latest Origin ACL IPs from TEO, creates Address Templates and Address Template Groups in VPC, and updates the specified Security Group ingress rule to allow traffic from these IPs.

## Features

- **Automatic IP Fetching**: Retrieves the latest IPv4 and IPv6 addresses from Tencent Cloud TEO.
- **VPC Address Management**: Automatically creates and manages VPC Address Templates and Address Template Groups.
- **Security Group Update**: Updates a specific Security Group rule to point to the new Address Template Group.
- **Cleanup**: Automatically removes old Address Templates and Groups to keep the VPC clean.
- **Multi-Zone Support**: Supports monitoring multiple TEO Zones.

## Prerequisites

- Python 3.12+
- Tencent Cloud Account with TEO and VPC permissions.
- **Security Group Rule**: You must pre-create an ingress rule in your Security Group with the description (remark) starting with `TEO Node`. This rule serves as a placeholder and will be updated by the tool.
  - Example: Allow `0.0.0.0/0` on port `443` with description `TEO Node`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OVINC/RefreshTEONodeIP.git
   cd RefreshTEONodeIP
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Configure the tool using environment variables. You can set these in your shell or use a `.env` file (if supported by your runner).

| Variable | Description | Required | Default |
|----------|-------------|:--------:|---------|
| `SECRET_ID` | Tencent Cloud Secret ID | Yes | - |
| `SECRET_KEY` | Tencent Cloud Secret Key | Yes | - |
| `REGION` | Tencent Cloud Region | No | `ap-guangzhou` |
| `TEO_ZONE_IDS` | Comma-separated list of TEO Zone IDs | Yes | - |
| `SECURITY_GROUP_ID` | The ID of the Security Group to update | Yes | - |
| `SECURITY_GROUP_PROTOCOL` | Protocol for the security group rule | No | `TCP` |
| `SECURITY_GROUP_PORT` | Port for the security group rule | No | `443` |
| `TEO_ADDRESS_TEMPLATE_MAX_ITEMS` | Max IPs per Address Template | No | `20` |
| `QUERY_LIMIT` | API Query Limit | No | `20` |
| `DEBUG` | Enable debug mode | No | `false` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

## Permissions

The Tencent Cloud CAM user requires the following permissions:

- `teo:DescribeOriginACL`
- `teo:ConfirmOriginACLUpdate`
- `vpc:DescribeAddressGroups`
- `vpc:DescribeAddress`
- `vpc:CreateAddress`
- `vpc:CreateAddressGroup`
- `vpc:CreateAddressTemplate`
- `vpc:CreateAddressTemplateGroup`
- `vpc:DeleteAddress`
- `vpc:DeleteAddressGroup`
- `vpc:DeleteAddressTemplate`
- `vpc:DeleteAddressTemplateGroup`
- `vpc:DescribeAddressTemplateGroups`
- `vpc:DescribeAddressTemplates`
- `cvm:DescribeSecurityGroupPolicys`
- `cvm:ModifySingleSecurityGroupPolicy`
- `cvm:ReplaceSecurityGroupPolicy`

## Usage

### Run Locally

```bash
export SECRET_ID="your_secret_id"
export SECRET_KEY="your_secret_key"
export TEO_ZONE_IDS="zone-id-1,zone-id-2"
export SECURITY_GROUP_ID="sg-xxxxxx"

python main.py
```

### Run with Docker

```bash
docker run -d \
  -e SECRET_ID="your_secret_id" \
  -e SECRET_KEY="your_secret_key" \
  -e TEO_ZONE_IDS="zone-id-1" \
  -e SECURITY_GROUP_ID="sg-xxxxxx" \
  ghcr.io/ovinc/refreshteonodeip:latest
```

## How it Works

1. **Fetch IPs**: Queries `DescribeOriginACL` for all configured `TEO_ZONE_IDS`.
2. **Create Templates**: Creates VPC Address Templates for the fetched IPs.
3. **Create Group**: Creates a VPC Address Template Group containing the new templates.
4. **Update Security Group**: Finds the ingress rule in `SECURITY_GROUP_ID` with the description starting with "TEO Node" and updates it to use the new Address Template Group.
5. **Confirm Update**: If TEO had a pending ACL update, it calls `ConfirmOriginACLUpdate`.
6. **Cleanup**: Deletes old Address Template Groups and Address Templates created by this tool.

## License

[MIT](LICENSE)

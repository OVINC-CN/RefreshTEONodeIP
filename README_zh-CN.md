# Refresh TEO Node IP (刷新 TEO 节点 IP)

此工具用于自动刷新 VPC 安全组中的腾讯云 TEO (EdgeOne) 节点 IP。它从 TEO 获取最新的回源 ACL IP，在 VPC 中创建 IP 地址模板和地址模板组，并更新指定的安全组入站规则以允许来自这些 IP 的流量。

## 功能特性

- **自动获取 IP**: 从腾讯云 TEO 获取最新的 IPv4 和 IPv6 地址。
- **VPC 地址管理**: 自动创建和管理 VPC IP 地址模板及地址模板组。
- **安全组更新**: 更新特定的安全组规则，将其指向新的地址模板组。
- **自动清理**: 自动删除旧的地址模板和地址模板组，保持 VPC 整洁。
- **多站点支持**: 支持同时监控多个 TEO 站点 (Zone)。

## 前置要求

- Python 3.12+
- 拥有 TEO 和 VPC 权限的腾讯云账号。
- **安全组规则**: 您必须在安全组中预先创建一个备注（描述）以 `TEO Node` 开头的入站规则。此规则作为占位符，将被工具更新。
  - 示例：创建一个允许 `0.0.0.0/0` 访问 `443` 端口的规则，并将其备注设置为 `TEO Node`。

## 安装

1. 克隆仓库:
   ```bash
   git clone https://github.com/OVINC/RefreshTEONodeIP.git
   cd RefreshTEONodeIP
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

## 配置

通过环境变量配置工具。

| 变量名 | 描述 | 是否必须 | 默认值 |
|----------|-------------|:--------:|---------|
| `SECRET_ID` | 腾讯云 Secret ID | 是 | - |
| `SECRET_KEY` | 腾讯云 Secret Key | 是 | - |
| `REGION` | 腾讯云地域 | 否 | `ap-guangzhou` |
| `TEO_ZONE_IDS` | TEO 站点 ID 列表 (逗号分隔) | 是 | - |
| `SECURITY_GROUP_ID` | 需要更新的安全组 ID | 是 | - |
| `SECURITY_GROUP_PROTOCOL` | 安全组规则协议 | 否 | `TCP` |
| `SECURITY_GROUP_PORT` | 安全组规则端口 | 否 | `443` |
| `TEO_ADDRESS_TEMPLATE_MAX_ITEMS` | 每个地址模板的最大 IP 数 | 否 | `20` |
| `QUERY_LIMIT` | API 查询分页限制 | 否 | `20` |
| `DEBUG` | 启用调试模式 | 否 | `false` |
| `LOG_LEVEL` | 日志级别 | 否 | `INFO` |

## 权限要求

腾讯云 CAM 用户需要以下权限：

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

## 使用方法

### 本地运行

```bash
export SECRET_ID="your_secret_id"
export SECRET_KEY="your_secret_key"
export TEO_ZONE_IDS="zone-id-1,zone-id-2"
export SECURITY_GROUP_ID="sg-xxxxxx"

python main.py
```

### Docker 运行

```bash
docker run -d \
  -e SECRET_ID="your_secret_id" \
  -e SECRET_KEY="your_secret_key" \
  -e TEO_ZONE_IDS="zone-id-1" \
  -e SECURITY_GROUP_ID="sg-xxxxxx" \
  ghcr.io/ovinc/refreshteonodeip:latest
```

## 工作原理

1. **获取 IP**: 查询所有配置的 `TEO_ZONE_IDS` 的 `DescribeOriginACL` 接口。
2. **创建模板**: 为获取到的 IP 创建 VPC IP 地址模板。
3. **创建组**: 创建包含新模板的 VPC IP 地址模板组。
4. **更新安全组**: 在 `SECURITY_GROUP_ID` 中查找描述以 "TEO Node" 开头的入站规则，并将其更新为使用新的地址模板组。
5. **确认更新**: 如果 TEO 有待确认的 ACL 更新，调用 `ConfirmOriginACLUpdate` 进行确认。
6. **清理**: 删除此工具创建的旧地址模板组和地址模板。

## 许可证

[MIT](LICENSE)

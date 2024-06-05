#!/bin/sh

API_ID=""
API_TOKEN=""
DOMAIN=""
TXT_VALUE=""

# 提取主域和子域
SUB_DOMAIN="_acme-challenge"
if [[ "$DOMAIN" =~ \. ]]; then
  BASE_DOMAIN=$(echo "$DOMAIN" | awk -F '.' '{print $(NF-1)"."$NF}')
  SUB_DOMAIN="_acme-challenge.${DOMAIN%.$BASE_DOMAIN}"
else
  BASE_DOMAIN="$DOMAIN"
fi

# 添加 TXT 记录
RESPONSE=$(curl -s -X POST https://dnsapi.cn/Record.Create \
  -d "login_token=${API_ID},${API_TOKEN}" \
  -d "format=json" \
  -d "domain=${BASE_DOMAIN}" \
  -d "sub_domain=${SUB_DOMAIN}" \
  -d "record_type=TXT" \
  -d "value=${TXT_VALUE}" \
  -d "record_line=默认")

if echo "$RESPONSE" | grep -q "\"code\":\"1\""; then
  echo "DNS TXT record created successfully."
else
  echo "Failed to create DNS TXT record: $RESPONSE"
  exit 1
fi

# 等待 DNS 生效
sleep 20
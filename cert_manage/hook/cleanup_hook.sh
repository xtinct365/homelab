#!/bin/bash

API_ID=""
API_TOKEN=""
DOMAIN=""

# 提取主域和子域
SUB_DOMAIN="_acme-challenge"
if [[ "$DOMAIN" =~ \. ]]; then
  BASE_DOMAIN=$(echo "$DOMAIN" | awk -F '.' '{print $(NF-1)"."$NF}')
  SUB_DOMAIN="_acme-challenge.${DOMAIN%.$BASE_DOMAIN}"
else
  BASE_DOMAIN="$DOMAIN"
fi

# 获取记录 ID
RECORD_ID=$(curl -s -X POST https://dnsapi.cn/Record.List \
  -d "login_token=${API_ID},${API_TOKEN}" \
  -d "format=json" \
  -d "domain=${BASE_DOMAIN}" \
  -d "sub_domain=${SUB_DOMAIN}" | jq -r '.records[] | select(.type == "TXT") | .id')

# 删除 TXT 记录
if [ -n "$RECORD_ID" ]; then
  curl -s -X POST https://dnsapi.cn/Record.Remove \
    -d "login_token=${API_ID},${API_TOKEN}" \
    -d "format=json" \
    -d "domain=${BASE_DOMAIN}" \
    -d "record_id=${RECORD_ID}"
  echo "DNS TXT record removed."
else
  echo "No matching DNS TXT record found to remove."
fi
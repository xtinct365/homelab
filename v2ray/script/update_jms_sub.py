import requests
import base64
import urllib3
import json
import docker
import os.path

urllib3.disable_warnings()

V2RAY_CONFIG_PATH = "/volume1/docker/v2ray/config"

VMESS_SERVER = {
    "user_id": "cba46381-ccef-4817-8ca4-f3bdb879cf75",
    "alter_id": 0,
    "security": "aes-128-gcm",
    "port": 7571,
    "server": {
        "usa": {
            "ip": "0.0.0.0",
            "config_path": os.path.join(V2RAY_CONFIG_PATH, "jms_usa.json"),
            "container_name": "v2ray_usa"
        },
        "jpn": {
            "ip": "0.0.0.0",
            "config_path": os.path.join(V2RAY_CONFIG_PATH, "jms_usa.json"),
            "container_name": "v2ray_jpn"
        },
        "nld": {
            "ip": "0.0.0.0",
            "config_path": os.path.join(V2RAY_CONFIG_PATH, "jms_usa.json"),
            "container_name": "v2ray_nld"
        }
    }
}

def add_padding_and_decode(base64_bytes):
    # Add padding if needed
    padding_needed = len(base64_bytes) % 4
    if padding_needed:
        base64_bytes += b'=' * (4 - padding_needed)

    # Decode the base64 string
    decoded_bytes = base64.b64decode(base64_bytes)
    return decoded_bytes


def get_container(name):
    docker_client = docker.from_env()

    try:
        ctn = docker_client.containers.get(name)
    except docker.errors.NotFound:
        ctn = None
    
    docker_client.close()

    return ctn


def process_vmess_server(resp):
    decoded_content = base64.b64decode(resp)
    for line in decoded_content.splitlines():
        if line.startswith(b"vmess"):
            vmess_bytes = add_padding_and_decode(line[8:])
            vmess = json.loads(vmess_bytes)
            if "c77s3" in vmess["ps"]:
                VMESS_SERVER["server"]["usa"]["ip"] = vmess["add"]
            elif "c77s4" in vmess["ps"]:
                VMESS_SERVER["server"]["jpn"]["ip"] = vmess["add"]
            elif "c77s5" in vmess["ps"]:
                VMESS_SERVER["server"]["nld"]["ip"] = vmess["add"]

# 设置请求头和参数
url = 'https://jmssub.net/members/getsub.php?service=526952&id=cba46381-ccef-4817-8ca4-f3bdb879cf75'

# 发送 POST 请求
response = requests.get(url, verify=False, timeout=10)

# 检查响应状态码
if response.status_code != 200:
    raise RuntimeError(f"Error: {response.status_code}, {response.content}")

#content = b'c3M6Ly9ZV1Z6TFRJMU5pMW5ZMjA2UjBGRFFuRjVNemN6VTB4b1pGcHJZMEEyTlM0ME9TNHlNREV1TmpNNk56VTNNUSNKTVMtNTI2OTUyQGM3N3MxLnBvcnRhYmxlc3VibWFyaW5lcy5jb206NzU3MQpzczovL1lXVnpMVEkxTmkxblkyMDZSMEZEUW5GNU16Y3pVMHhvWkZwclkwQXhPVGt1TVRFMUxqSXlPUzQxTXpvM05UY3gjSk1TLTUyNjk1MkBjNzdzMi5wb3J0YWJsZXN1Ym1hcmluZXMuY29tOjc1NzEKdm1lc3M6Ly9leUp3Y3lJNklrcE5VeTAxTWpZNU5USkFZemMzY3pNdWNHOXlkR0ZpYkdWemRXSnRZWEpwYm1WekxtTnZiVG8zTlRjeElpd2ljRzl5ZENJNklqYzFOekVpTENKcFpDSTZJbU5pWVRRMk16Z3hMV05qWldZdE5EZ3hOeTA0WTJFMExXWXpZbVJpT0RjNVkyWTNOU0lzSW1GcFpDSTZNQ3dpYm1WMElqb2lkR053SWl3aWRIbHdaU0k2SW01dmJtVWlMQ0owYkhNaU9pSnViMjVsSWl3aVlXUmtJam9pT1RVdU1UWTVMakkzTGpreUluMAp2bWVzczovL2V5SndjeUk2SWtwTlV5MDFNalk1TlRKQVl6YzNjelF1Y0c5eWRHRmliR1Z6ZFdKdFlYSnBibVZ6TG1OdmJUbzNOVGN4SWl3aWNHOXlkQ0k2SWpjMU56RWlMQ0pwWkNJNkltTmlZVFEyTXpneExXTmpaV1l0TkRneE55MDRZMkUwTFdZelltUmlPRGM1WTJZM05TSXNJbUZwWkNJNk1Dd2libVYwSWpvaWRHTndJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSjBiSE1pT2lKdWIyNWxJaXdpWVdSa0lqb2lNVGM0TGpFMU55NDFOaTR5TWlKOQp2bWVzczovL2V5SndjeUk2SWtwTlV5MDFNalk1TlRKQVl6YzNjelV1Y0c5eWRHRmliR1Z6ZFdKdFlYSnBibVZ6TG1OdmJUbzNOVGN4SWl3aWNHOXlkQ0k2SWpjMU56RWlMQ0pwWkNJNkltTmlZVFEyTXpneExXTmpaV1l0TkRneE55MDRZMkUwTFdZelltUmlPRGM1WTJZM05TSXNJbUZwWkNJNk1Dd2libVYwSWpvaWRHTndJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSjBiSE1pT2lKdWIyNWxJaXdpWVdSa0lqb2lNVFl5TGpJME9DNDNOaTQwT1NKOQp2bWVzczovL2V5SndjeUk2SWtwTlV5MDFNalk1TlRKQVl6YzNjemd3TVM1d2IzSjBZV0pzWlhOMVltMWhjbWx1WlhNdVkyOXRPamMxTnpFaUxDSndiM0owSWpvaU56VTNNU0lzSW1sa0lqb2lZMkpoTkRZek9ERXRZMk5sWmkwME9ERTNMVGhqWVRRdFpqTmlaR0k0TnpsalpqYzFJaXdpWVdsa0lqb3dMQ0p1WlhRaU9pSjBZM0FpTENKMGVYQmxJam9pYm05dVpTSXNJblJzY3lJNkltNXZibVVpTENKaFpHUWlPaUkwTlM0Mk1pNHhNREF1TVRVaWZR'
process_vmess_server(response.content)

for server_cfg in VMESS_SERVER["server"].values():
    container = get_container(server_cfg["container_name"])
    if container is None or container.status != "running":
        continue

    with open(server_cfg["config_path"], "r") as f:
        curr_cfg = json.load(f)
    if curr_cfg is None:
        continue
    curr_ip = curr_cfg["outbounds"][0]["settings"]["vnext"][0]["address"]
    new_ip = server_cfg["ip"]
    if curr_ip != new_ip:
        curr_cfg["outbounds"][0]["settings"]["vnext"][0]["address"] = new_ip
        curr_cfg["outbounds"][0]["settings"]["vnext"][0]["port"] = VMESS_SERVER["port"]
        curr_cfg["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = VMESS_SERVER["user_id"]
        curr_cfg["outbounds"][0]["settings"]["vnext"][0]["users"][0]["alterId"] = VMESS_SERVER["alter_id"]
        curr_cfg["outbounds"][0]["settings"]["vnext"][0]["users"][0]["security"] = VMESS_SERVER["security"]
        with open(server_cfg["config_path"], "w") as f:
            json.dump(curr_cfg, f, indent=2)
        container.restart()

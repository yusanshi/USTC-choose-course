# Educational administration system information
USERNAME = 'PBXXXXXXXX'
PASSWORD = ''

# Retry MAX_TIME times on error
MAX_TIME = 10

# Send mail
# e.g. send from 00000000@163.com to 00000000@qq.com
SMTP_HOST = 'smtp.163.com'
SMTP_PORT = 465
SMTP_USERNAME = '00000000@163.com'  # SMTP 用户名
SMTP_PASSWORD = '123456'  # SMTP 密码（部分邮箱需要填写授权码而不是登录密码）
SENDER = '00000000@163.com'
RECEIVER = '00000000@qq.com'

# Headers used in GET/POST request. No need to modify.
HEADERS = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

HEADERS_JSON = {
    'content-type': 'application/json;charset=utf-8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

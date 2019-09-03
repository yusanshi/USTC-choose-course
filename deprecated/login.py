import requests
from config import HEADERS, USERNAME, PASSWORD


def login():
    url = 'https://passport.ustc.edu.cn/login?service=https://jw.ustc.edu.cn/ucas-sso/login'

    data = {
        'model': 'uplogin.jsp',
        'service': 'https://jw.ustc.edu.cn/ucas-sso/login',
        'warn': '',
        'showCode': '',
        'username': USERNAME,
        'password': PASSWORD,
        'button': '',
    }

    session = requests.Session()
    html = session.post(url, headers=HEADERS,
                        data=data, allow_redirects=False)
    session2 = requests.Session()
    session2.get(
        html.headers['location'], headers=HEADERS, allow_redirects=False)
    return session2


if __name__ == "__main__":
    # if no error, OK!
    login()

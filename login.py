import requests
import easyocr
import warnings

from bs4 import BeautifulSoup
from config import USERNAME, PASSWORD

CAS_LOGIN_URL = 'https://passport.ustc.edu.cn/login'
CAS_CAPTCHA_URL = 'https://passport.ustc.edu.cn/validatecode.jsp?type=login'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

ocr_reader = easyocr.Reader(['en'])

warnings.filterwarnings('ignore', category=UserWarning)


def login(service_url):
    s = requests.Session()
    s.headers['User-Agent'] = USER_AGENT

    r = s.get(CAS_LOGIN_URL, params={'service': service_url})
    cas_lt = BeautifulSoup(r.text, 'lxml').find(id='CAS_LT')['value']

    r = s.get(CAS_CAPTCHA_URL)
    image = r.content

    captcha = ocr_reader.readtext(image, detail=0, allowlist='0123456789')[0]
    print('Captcha recognized: {}'.format(captcha))

    data = {
        'model': 'uplogin.jsp',
        'service': service_url,
        'warn': '',
        'showCode': '1',
        'username': USERNAME,
        'password': PASSWORD,
        'button': '',
        'CAS_LT': cas_lt,
        'LT': captcha,
    }
    s.post(CAS_LOGIN_URL, data=data)
    return s


if __name__ == '__main__':
    # 使用研究生身份信息以测试
    session = login('https://yjs.ustc.edu.cn/default.asp')
    assert '姓名' in session.get('https://yjs.ustc.edu.cn/m_top.asp').text

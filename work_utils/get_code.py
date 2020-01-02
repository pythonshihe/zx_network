import requests
import time
import json
import random

s = requests

z_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
          'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
          'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
          'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
          'x', 'y', 'z']
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
}


def get_img():
    url2 = 'http://zxgk.court.gov.cn/xgl/captchaXgl.do?captchaId={}&random={}'
    random_num = random.random() + random.randint(1, 9) * 0.00000000000000001
    num = ''
    for i in range(0, 32):
        random_num = random.random()
        value_num = int(random_num * 61)
        num += z_list[value_num]
    url = url2.format(num, random_num)
    k = True
    while k:
        try:
            response_text = s.get(url=url, headers=headers)
            # response_text = s.get(url=url, headers=headers)
            response_img = response_text.content
            with open('code.jpg', 'wb') as f:
                f.write(response_img)
            return {'code_img': response_img, 'captchaId': num, 'random_num': random_num}
        except Exception as e:
            time.sleep(0.2)
            # print(repr(e))


# 识别验证码
def correct_code():
    while True:
        data_dict = get_img()
        code_img = data_dict.get('code_img')
        captcha_id = data_dict.get('captchaId')
        proxies = data_dict.get('proxies')
        result_code = requests.post(url='http://********:18080', data=code_img).text
        code = json.loads(result_code).get('code')
        if code:
            # print('验证码', code)
            return code, captcha_id
        else:
            time.sleep(20)


if __name__ == '__main__':
    code, captcha_id = correct_code()
    # print(code)
    # print(captcha_id)

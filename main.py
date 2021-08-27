import json
import time
import argparse

from random import uniform
from distutils.util import strtobool
from login import login
from send_mail import send_mail
from config import USERNAME, MAX_TIME


class Selector:
    def __init__(self, identity):
        self.identity = identity
        self.login()
        self.student_ID = self.get_student_ID()
        self.course_select_turn_ID = self.get_course_select_turn_ID()
        self.addable_lessons = self.get_addable_lessons()

    def login(self):
        if self.identity == 'undergraduate':
            service_url = 'https://jw.ustc.edu.cn/ucas-sso/login'
        elif self.identity == 'postgraduate':
            service_url = 'https://yjs.ustc.edu.cn/default.asp'
        else:
            raise ValueError
        self.session = login(service_url)

    def get_student_ID(self):
        if self.identity == 'undergraduate':
            url = 'https://jw.ustc.edu.cn/for-std/course-select'
        elif self.identity == 'postgraduate':
            ASPSESSIONIDCSAASBCS = self.session.cookies.get(
                'ASPSESSIONIDCSAASBCS')
            url = f'https://jw.ustc.edu.cn/graduate-login?stn={USERNAME}&ASPSESSIONIDCSAASBCS={ASPSESSIONIDCSAASBCS}'
        else:
            raise ValueError

        r = self.session.get(url)
        return r.url.split('/')[-1]

    def get_course_select_turn_ID(self):
        if self.identity == 'undergraduate':
            bizTypeId = '2'
        elif self.identity == 'postgraduate':
            bizTypeId = '3'
        else:
            raise ValueError

        data = {
            'bizTypeId': bizTypeId,
            'studentId': self.student_ID,
        }
        url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/open-turns'
        r = self.session.post(url, data=data)
        r = json.loads(r.text)
        assert len(r) == 1
        return r[0]['id']

    def get_addable_lessons(self):
        url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/addable-lessons'
        data = {
            'turnId': self.course_select_turn_ID,
            'studentId': self.student_ID
        }
        r = self.session.post(url, data=data)
        return json.loads(r.text)

    def get_course_info(self, course_code):
        for item in self.addable_lessons:
            if item['code'] == course_code:
                course_ID = str(item['id'])
                course_name = item['course']['nameZh']
                course_teacher = ' '.join(teacher['nameZh']
                                          for teacher in item['teachers'])
                return course_ID, course_name, course_teacher
        return None, None, None

    def process_request_ID(self, request_ID):
        url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/add-drop-response'
        data = {'studentId': self.student_ID, 'requestId': request_ID}

        r = self.session.post(url, data=data)
        return json.loads(r.text)


class DirectSelector(Selector):
    def __init__(self, new_course_code, period, stable_mode, identity):
        super().__init__(identity)
        self.new_course_code = new_course_code
        self.period = period
        self.stable_mode = stable_mode
        self.new_course_ID, self.new_course_name, self.new_course_teacher = self.get_course_info(
            self.new_course_code)

    def work(self):
        print(f'开始选 {self.new_course_teacher} 的《{self.new_course_name}》...')

        count = 1
        while True:
            print(f'正在第 {count} 次尝试...')
            count += 1

            if self.stable_mode:
                print('重新登录中...')
                self.login()
                # Must add this, or new 'session' can't get/post in following request
                self.get_student_ID()

            url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/add-request'
            data = {
                'studentAssoc': self.student_ID,
                'lessonAssoc': self.new_course_ID,
                'courseSelectTurnAssoc': self.course_select_turn_ID,
                'scheduleGroupAssoc': '',
                'virtualCost': '0'
            }

            # TODO: 用约 2 行代码获取 request_ID
            request_ID = 'request_ID'

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))

            result = self.process_request_ID(request_ID)

            if result is None:
                print('响应为空，重试...')
            elif result['success'] is True:
                message = f'成功选择 {self.new_course_teacher} 的《{self.new_course_name}》，程序退出！'
                print(message)
                send_mail(message, message)
                break
            else:
                print('直选失败，失败原因： ' + result['errorMessage']['textZh'])

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))


class CourseChanger(Selector):
    def __init__(self, new_course_code, period, old_course_code, reason,
                 stable_mode, identity):
        super().__init__(identity)
        self.new_course_code = new_course_code
        self.period = period
        self.old_course_code = old_course_code
        self.reason = reason
        self.stable_mode = stable_mode
        self.new_course_ID, self.new_course_name, self.new_course_teacher = self.get_course_info(
            self.new_course_code)
        self.old_course_ID, self.old_course_name, self.old_course_teacher = self.get_course_info(
            self.old_course_code)
        self.semester_ID = self.get_semester_ID()

    def get_semester_ID(self):
        raise NotImplementedError

    def work(self):
        print(
            f'开始将《{self.new_course_name}》从 {self.old_course_teacher} 换到 {self.new_course_teacher}'
        )
        count = 1
        while True:
            print(f'正在第 {count} 次尝试...')
            count += 1

            if self.stable_mode:
                print('重新登录中...')
                self.login()
                # Must add this, or new 'session' can't get/post in following request
                self.get_student_ID()

            raise NotImplementedError

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))

            result = self.process_request_ID(request_ID)

            if result is None:
                print('响应为空，重试...')
            elif result['success'] is True:
                message = f'成功换班到 {self.new_course_teacher} 的《{self.new_course_name}》，程序退出！'
                print(message)
                send_mail(message, message)
                break
            else:
                print('换班失败，失败原因： ' + result['errorMessage']['textZh'])

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))


def main():
    parser = argparse.ArgumentParser(
        description=
        'Support choosing course directly or changing course. If choosing course, provide new course code. If changing course, also provide old course code and reason to change.'
    )
    parser.add_argument('new_course_code',
                        type=str,
                        help='New course code, e.g. PE00120.02')
    parser.add_argument('old_course_code',
                        type=str,
                        nargs='?',
                        help='Old course code, e.g. PE00120.01')
    parser.add_argument('reason',
                        type=str,
                        nargs='?',
                        default='',
                        help='Reason to change course (not necessary)')
    parser.add_argument('-p',
                        '--period',
                        type=float,
                        default=5.0,
                        help='Specify a period. (unit: second, default: 5.0)')
    parser.add_argument(
        '-s',
        '--stable_mode',
        type=lambda x: bool(strtobool(x)),
        default=False,
        help=
        'Whether to enable stable mode. If enabled, this script will relogin after each try (default: False)'
    )
    parser.add_argument(
        '-i',
        '--identity',
        type=str,
        default='undergraduate',
        choices=['undergraduate', 'postgraduate'],
        help=
        'Your identity, undergraduate or postgraduate (default: undergraduate)'
    )
    args = parser.parse_args()
    print(args)

    if args.old_course_code is None:
        worker = DirectSelector(args.new_course_code, args.period,
                                args.stable_mode, args.identity)
    else:
        raise NotImplementedError
        worker = CourseChanger(args.new_course_code, args.period,
                               args.old_course_code, args.reason,
                               args.stable_mode, args.identity)

    for i in range(MAX_TIME):
        try:
            worker.work()
            break
        except Exception as e:
            timestamp = time.asctime(time.localtime(time.time()))
            title = f'第 {i + 1} 次出现异常！ {timestamp}'
            body = f'{str(e)} {timestamp}'
            print(title)
            print(body)
            send_mail(title, body)
            time.sleep(30)
    else:
        message = '异常次数达到最大值，程序退出！'
        print(message)
        send_mail(message, message)


if __name__ == '__main__':
    main()

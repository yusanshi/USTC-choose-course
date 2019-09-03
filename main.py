import requests
import json
import re
import time
import argparse
from bs4 import BeautifulSoup
from random import uniform
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import *


class Mail_Sender:
    def send_mail(self, title, body):
        message = MIMEText('<h1>' + body + '</h1>', 'html', 'utf-8')
        message['From'] = SENDER
        message['To'] = RECEIVER
        message['Subject'] = Header(title, 'utf-8')

        smtpObj = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        smtpObj.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtpObj.sendmail(SENDER,
                         [RECEIVER], message.as_string())
        smtpObj.quit()


class Selector:
    def __init__(self):
        self.brow = self.login()
        self.sender = Mail_Sender()
        self.student_ID = self.get_student_ID()
        self.course_select_Turn_ID = self.get_course_select_Turn_ID()
        self.addable_lessons_json = self.get_addable_lessons_json()

    def login(self):
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

    def relogin(self):
        self.brow = self.login()

    def get_student_ID(self):
        course_select = 'https://jw.ustc.edu.cn/for-std/course-select'
        temp = self.brow.get(
            course_select, headers=HEADERS, allow_redirects=False)
        return temp.headers['location'].split('/')[-1]

    def get_course_select_Turn_ID(self):
        data_for_open_turn = {
            'bizTypeId': '2',
            'studentId': self.student_ID,
        }
        open_turns = 'https://jw.ustc.edu.cn/ws/for-std/course-select/open-turns'
        temp_1 = self.brow.post(open_turns, headers=HEADERS,
                                data=data_for_open_turn, allow_redirects=False)
        temp_2 = BeautifulSoup(temp_1.text, 'lxml')
        temp_2 = json.loads(temp_2.p.string)
        return str(temp_2[0]['id'])

    def get_addable_lessons_json(self):
        get_ID_url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/addable-lessons'
        get_ID_data = {
            'turnId': self.course_select_Turn_ID,
            'studentId': self.student_ID
        }
        addable_lessons = self.brow.post(
            get_ID_url, data=get_ID_data, headers=HEADERS, allow_redirects=False)
        return json.loads(addable_lessons.text)

    def parse_from_code(self, course_code):
        course_ID = None
        course_name = None
        course_teacher = None
        if course_code != None:
            for item in self.addable_lessons_json:
                if item['code'] == course_code:
                    course_ID = str(item['id'])
                    course_name = item['course']['nameZh']
                    course_teacher = ' '.join(
                        teacher['nameZh'] for teacher in item['teachers'])
                    break

        return course_ID, course_name, course_teacher

    def process_request_ID(self, request_ID):
        add_drop_url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/add-drop-response'
        add_drop_data = {
            'studentId': self.student_ID,
            'requestId': request_ID
        }

        temp_5 = self.brow.post(add_drop_url, data=add_drop_data,
                                headers=HEADERS, allow_redirects=False)
        temp_5 = BeautifulSoup(temp_5.text, 'lxml')
        result = json.loads(temp_5.p.string)
        return result


class Direct_Selector(Selector):
    def __init__(self, new_course_code, period, stable_mode):
        super().__init__()
        self.new_course_code = new_course_code
        self.period = period
        self.stable_mode = stable_mode
        self.new_course_ID, self.new_course_name, self.new_course_teacher = self.parse_from_code(
            self.new_course_code)

    def work(self):
        print("开始选 %s 的《%s》..." %
              (self.new_course_teacher, self.new_course_name))

        count = 1
        while True:
            print("正在第 %d 次尝试..." % count)
            count += 1

            if self.stable_mode:
                print("重新登录中...")
                self.relogin()
                # Must add this, or new "brow" can't get/post in following request
                self.get_student_ID()

            seletion_url = 'https://jw.ustc.edu.cn/ws/for-std/course-select/add-request'
            seletion_data = {
                'studentAssoc': self.student_ID,
                'lessonAssoc': self.new_course_ID,
                'courseSelectTurnAssoc': self.course_select_Turn_ID,
                'scheduleGroupAssoc': '',
                'virtualCost': '0'
            }

            # TODO
            # 此处删掉的内容约 3 行左右，
            # 用于得到直选课时的 request_ID

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))

            result = self.process_request_ID(request_ID)

            if result == None:
                print("响应为空，重试...")
            elif result['success'] == True:
                message = "成功选择 %s 的《%s》，程序退出！" % (
                    self.new_course_teacher, self.new_course_name)
                print(message)
                self.sender.send_mail(message, message)
                break
            else:
                print("直选失败，失败原因： " + result['errorMessage']['textZh'])

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))


class Course_Changer(Selector):
    def __init__(self, new_course_code, period, old_course_code, reason, stable_mode):
        super().__init__()
        self.new_course_code = new_course_code
        self.period = period
        self.old_course_code = old_course_code
        self.reason = reason
        self.stable_mode = stable_mode
        self.new_course_ID, self.new_course_name, self.new_course_teacher = self.parse_from_code(
            self.new_course_code)
        self.old_course_ID, self.old_course_name, self.old_course_teacher = self.parse_from_code(
            self.old_course_code)
        self.semester_ID = self.get_semester_ID()

    def get_semester_ID(self):
        course_select = 'https://jw.ustc.edu.cn/for-std/course-select'
        url_temp = course_select + '/' + self.student_ID + \
            '/turn/' + self.course_select_Turn_ID + '/select'
        semester_ID_temp = self.brow.get(
            url_temp, headers=HEADERS, allow_redirects=False)
        semester_ID = BeautifulSoup(semester_ID_temp.text, 'lxml')
        semester_ID = str(semester_ID)
        pattern = re.compile(r'semesterId:\s\d{1,5},')
        semester_ID = pattern.findall(semester_ID)
        assert len(semester_ID) == 1
        pattern_2 = re.compile(r'\d+')
        return pattern_2.findall(semester_ID[0])[0]

    def work(self):
        print("开始将《%s》从 %s 换到 %s" %
              (self.new_course_name, self.old_course_teacher, self.new_course_teacher))

        count = 1
        while True:
            print("正在第 %d 次尝试..." % count)
            count += 1

            if self.stable_mode:
                print("重新登录中...")
                self.relogin()
                # Must add this, or new "brow" can't get/post in following request
                self.get_student_ID()
                
            pre_check_url = 'https://jw.ustc.edu.cn/for-std/course-adjustment-apply/preCheck'
            pre_check_data = [{
                'oldLessonAssoc': int(self.old_course_ID),
                'newLessonAssoc': int(self.new_course_ID),
                'studentAssoc': int(self.student_ID),
                'semesterAssoc': int(self.semester_ID),
                'bizTypeAssoc': 2,
                'applyReason': self.reason,
                'applyTypeAssoc': 5,
                'scheduleGroupAssoc': None
            }]
            pre_check_data = json.dumps(pre_check_data)

            self.brow.post(pre_check_url, data=pre_check_data,
                           headers=HEADERS_JSON, allow_redirects=False)

            change_url = 'https://jw.ustc.edu.cn/for-std/course-adjustment-apply/add-drop-request'
            change_data = {
                'studentAssoc': int(self.student_ID),
                'semesterAssoc': int(self.semester_ID),
                'bizTypeAssoc': 2,
                'applyTypeAssoc': 5,
                'checkFalseInsertApply': False,
                'lessonAndScheduleGroups': [{
                    'lessonAssoc': int(self.new_course_ID),
                    'dropLessonAssoc': int(self.old_course_ID),
                    'scheduleGroupAssoc': None
                }]
            }

            # TODO
            # 此处删掉的内容约 4 行左右，
            # 用于得到换班时的 request_ID
			
            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))

            result = self.process_request_ID(request_ID)

            if result == None:
                print("响应为空，重试...")
            elif result['success'] == True:
                message = "成功换班到 %s 的《%s》，程序退出！" % (
                    self.new_course_teacher, self.new_course_name)
                print(message)
                self.sender.send_mail(message, message)
                break
            else:
                print("换班失败，失败原因： " + result['errorMessage']['textZh'])

            time.sleep(self.period * 0.5 * uniform(0.6, 1.4))


def main():
    parser = argparse.ArgumentParser(
        description='Support choosing course directly or changing course. If choosing course, provide new course code. If changing course, also provide old course code and reason to change.')
    parser.add_argument("new_course_code", type=str,
                        help="New course code (i.e. PE00120.02)")
    parser.add_argument("old_course_code", type=str, nargs='?',
                        help="Old course code (i.e. PE00120.01)")
    parser.add_argument("reason", type=str, nargs='?',
                        help="Reason to change course")
    parser.add_argument(
        "-p", "--period", type=float, default=5.0, help="Specify a period. (unit: second, default: 5.0)")
    parser.add_argument(
        "-s", "--stable_mode", type=bool, default=False, help="Whether to enable stable mode. If enabled, this script will relogin after each try (default: False)")
    args = parser.parse_args()

    # print(args)

    worker = Direct_Selector(args.new_course_code, args.period, args.stable_mode) if args.old_course_code == None else Course_Changer(
        args.new_course_code, args.period, args.old_course_code, args.reason, args.stable_mode)

    for i in range(MAX_TIME):
        try:
            worker.work()
            break
        except Exception as e:
            timestamp = time.asctime(time.localtime(time.time()))
            title = "第 %d 次出现异常！ %s" % (i+1, timestamp)
            body = "%s %s" % (str(e), timestamp)
            print(title)
            print(body)
            worker.sender.send_mail(title, body)
            time.sleep(30)


if __name__ == "__main__":
    main()

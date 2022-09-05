import requests
import json


def search_courses(payload):
    """
    Go to ntust querycourse page to get the courses data
    :param payload: [Dict] The requests payload represent the options of the searching courses
    :return: [List] The courses data with json form
    """
    url = 'https://querycourse.ntust.edu.tw/querycourse/api/courses'

    # Set the requests header and cookies
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.102 Safari/537.36 ',
        'Content-Type': 'application/json; charset=utf-8'
    }
    cookies = {
        '.ASPXAUTH': '487D8DEBA53132B78A51A864286546F79151C74628A4ED4418850D0C03B6CE5FFC07F18AE'
                     'CE3B75B1D7DE9132A794D3C6C51FA2F61BDE3D4CD5FB4A845D16159D792BE67344C2B143B'
                     'CA2DF043F15EF113072A3C2EB4565748082DCD0BA54BCD8EF3D5C6A787E93F21E1CB937A0'
                     'E2632BFDD40301E62B81A53A53C2C35ED311FB0FC0D853FC6E76C727B2F0CAEC23AB03330'
                     'F76AF3FD3892E76C02F97F301B42E102D5E430E13E6B8CC90F6DB23D7F243BE38B3CE5A06'
                     'EA3449E4F32F71B492FFB784F24A899DAA39498510E333013D94051B0285445FFFB38C571'
                     'F5C3A05105F0E0C4934681D68BBD213FA81A3E8ACEDF2766123DED0ACCDA94ED699D915E1'
                     '37F6DF6D5DCD9BCFD68BB9F19E5E21D251B5572B3D31E64679C50121D3810B5E551C0D58E',
        'ntustsecret': '7166386161494A596458784974526457466C79524D643848524433654E6E3567',
        'ntustjwtsecret': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
                          '.eyJuYW1lIjoiQjEwNzMwMDMyIiwiZXhwIjoxNjAwMTU4ODM2LCJuYmYiOjE2MDAwNzI0MzZ9'
                          '.C6F3mYLp7yJflQHBUvS_zgRN1ZDnSXmlXJkHFAADizg '
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers, cookies=cookies)  # get the courses data
    api_data = json.loads(r.text)  # transform the data from json to list
    return api_data


def get_ntust_general_courses():
    """
    Get the NTUST general courses data
    :return: [List] The NTUST general courses data with json struct
    """
    payload = {
        'CourseName': "",
        'CourseNo': "",
        'CourseNotes': "",
        'CourseTeacher': "",
        'Dimension': "",
        'ForeignLanguage': 0,
        'Language': "zh",
        'OnleyNTUST': 1,
        'OnlyGeneral': 1,
        'OnlyMaster': 0,
        'Semester': "1101",
    }
    return search_courses(payload)


def get_ntu_system_courses():
    """
    Get the NTU system course data
    :return: [List] The NTU system course data with json struct
    """
    payload = {
        'CourseName': "",
        'CourseNo': "3",
        'CourseNotes': "",
        'CourseTeacher': "",
        'Dimension': "",
        'ForeignLanguage': 0,
        'Language': "zh",
        'OnleyNTUST': 0,
        'OnlyGeneral': 0,
        'OnlyMaster': 0,
        'OnlyNode': 0,
        'OnlyUnderGraduate': 0,
        'Semester': "1101",
    }
    return search_courses(payload)


def find_mba_course():
    payload = {
      "Semester": "1101",
      "CourseNo": "MA",
      "CourseName": "",
      "CourseTeacher": "",
      "Dimension": "",
      "CourseNotes": "",
      "ForeignLanguage": 0,
      "OnlyGeneral": 0,
      "OnleyNTUST": 0,
      "OnlyUnderGraduate": 0,
      "OnlyMaster": 0,
      "Language": "zh",
    }
    return search_courses(payload)

def get_all_course():
    """
    Get all ntust course data
    :return: [List] The all ntust course data with json struct
    """
    payload = {
        "CourseName": "",
        "CourseNo": "",
        "CourseNotes": "",
        "CourseTeacher": "",
        "Dimension": "",
        "ForeignLanguage": 0,
        "Language": "zh",
        "OnleyNTUST": 1,
        "OnlyGeneral": 0,
        "OnlyMaster": 0,
        "OnlyNode": 0,
        "OnlyUnderGraduate": 1,
        "Semester": "1111"
    }

def find_available(courses):
    """
    Find out the available courses
    :param courses: [List] The courses list
    :return: [List] The available courses list
    """
    available_courses = []
    for course in courses:
        if course['ChooseStudent'] < int(course['Restrict2']):
            available_courses.append(course)
    return available_courses


def output_result(result):
    """
    Transform the courses list to the line bot string
    :param result: [List] The courses list
    :return: [Str] The courses data after process, form "course_num course_name"
    """
    output = []
    for course in result:  # get the course_num & course_name
        output.append(course['CourseNo']+' '+course['CourseName'])
    str_out = '\n'.join(output)  # Transform the course data into string
    return str_out


def check_available(code):
    return code in [course['CourseNo'] for course in find_available(get_all_course())]


if __name__ == '__main__':
    for available_course in find_available(get_ntust_general_courses()):
        print(available_course['CourseName'])
    print("-----NTU System-----")
    for available_course in find_available(get_ntu_system_courses()):
        print(available_course['CourseName'])
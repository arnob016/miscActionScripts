import requests
import time
import os
import argparse
import re
from lxml import html
from threading import Thread


parser = argparse.ArgumentParser(
    description='Auto geting blc exp. Just for fun!')
parser.add_argument('-m', type=str, help='Your MoodleSession cookies!')
parser.add_argument(
    '-c', nargs='*', help='Your target courses links!')
parser.add_argument(
    '-n', action=argparse.BooleanOptionalAction, help='Hide your name!')
parser.add_argument('-u', type=str, help='Username')
parser.add_argument('-p', type=str, help='Password')
parser.add_argument(
    '-t', action=argparse.BooleanOptionalAction, help='Run in Thread')
parser.add_argument('--mark', action=argparse.BooleanOptionalAction,
                    help='Click all mark as completed')
args = parser.parse_args()

headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.46 Safari/537.36',
}

baseUrl = "https://elearn.daffodilvarsity.edu.bd"
session = requests.Session()

jar = requests.cookies.RequestsCookieJar()
jar.set('MoodleSession', args.m)


def login(user=args.u, passw=args.p):
    global s

    if not (user or passw):
        return False

    loginLink = f"{baseUrl}/login/index.php"
    s.cookies.clear()
    loginPage = s.get(loginLink, headers=headers).text
    tree = html.fromstring(loginPage)
    logintoken = tree.xpath(
        "//form[@id='login']/input[@name='logintoken']")[0].value
    loginTry = s.post(loginLink, data={
        "username": user,
        "password": passw,
        "logintoken": logintoken}, headers=headers)

    return True if loginTry.ok else False


def clear_output():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def sleep(s):
    print("")
    for i in range(s, 0, -1):
        print('-', end='')
        time.sleep(1)
    print("")


def sesskeyGet(allpageLink):
    return re.search(r"sesskey\"\:\"([^\"]+)", allpageLink, re.M).group(1)


def getAllEnrollCourse(mode="all"):
    allpageLink = s.get(f"{baseUrl}/my/", headers=headers).text
    sesskey = sesskeyGet(allpageLink)
    postUrl = fr"{baseUrl}/lib/ajax/service.php"

    data = s.post(
        postUrl,
        params={"sesskey": sesskey},
        json=[{"methodname": "core_course_get_enrolled_courses_by_timeline_classification",
               "args": {"classification": "all"}}], headers=headers).json()

    if mode == "all":
        return data
    elif mode == "links":
        courseLink = []
        for link in data[0]["data"]["courses"]:
            courseLink.append(link["viewurl"])
        return courseLink


def marksAsDone(allpageLink):
    tree = html.fromstring(allpageLink)
    sesskey = sesskeyGet(allpageLink)
    postUrl = fr"{baseUrl}/lib/ajax/service.php"

    cmids = tree.xpath(
        "//button[@data-action='toggle-manual-completion' and @data-toggletype='manual:mark-done']/@data-cmid")
    if cmids:
        for cmid in cmids:
            print(cmid, "->", s.post(
                postUrl,
                params={"sesskey": sesskey},
                json=[{"methodname": "core_completion_update_activity_completion_status_manually",
                  "args":
                      {"cmid": int(cmid),
                       "completed": True}
                       }], headers=headers).json()[0]['data']["status"])
    else:
        print("All Marks already Done")


def loginCheck():
    faildCheck = False
    if args.m:
        try:
            allpageLink = s.get(baseUrl+"/my", headers=headers).text
            tree = html.fromstring(allpageLink)
            if not tree.xpath("//span[@class='username pr-1']"):
                raise Exception("404")
            return True
        except:
            faildCheck = True

    if faildCheck or (not args.m):
        if login():
            return True
        else:
            return False


def job(l):
    eT = 0
    old = 0

    clickLink = []

    allpageLink = s.get(l, headers=headers).text
    tree = html.fromstring(allpageLink)

    print(tree.xpath("//h3[@class='page-title mb-0']")[0].text)
    if args.mark:
        marksAsDone(allpageLink)
    clickLink.append(l)
    clickLink += tree.xpath(
        "//div[@class='activityinstance']/a[@class='aalink']/@href")
    for ids, link in enumerate(clickLink):
        loop = ids
        trying = s.get(link, headers=headers)
        trylogin = trying.text
        if not trying.status_code == 200:
            if eT < 3:
                print(f"Retrying... {eT}")
                eT += 1
                continue
            else:
                clear_output()
                raise Exception(
                    f"Status code: {trying.status_code}\n count: {loop}\nLink: {link}")
        if ids == 0:
            tree = html.fromstring(trylogin)
            if not args.n:
                name = tree.xpath('//span[@class="username pr-1"]/text()')
            else:
                name = "Hidden"
            # Ex-show Use
            try:
                nowEx = int(tree.xpath(
                    '//div[@class="xp-total"]/div/div[@class="pts"]/text()')[0].replace(',', ''))
            except:
                nowEx = 0
            print(
                f"{name} xp:{nowEx-old if loop != 0 else 0}+ T:{nowEx}xp Loop:{loop} \n[0]", end='')
            if loop != 0 and (nowEx-old) == 0:
                sleep(5)

            old = nowEx

        else:
            print(f"[{ids}]", end='')
        sleep(5)


s = requests.Session()
s.cookies = jar


if loginCheck():
    if not args.c:
        courseLink = getAllEnrollCourse("links")
        print("courses>>", courseLink)
    else:
        courseLink = args.c

    if args.t:
        threadList = []
        for t in courseLink:
            threadList.append(Thread(target=job, args=(t,)))
        for _ in threadList:
            _.start()
        for _ in threadList:
            _.join()
    else:
        while True:
            for course in courseLink:
                job(course)

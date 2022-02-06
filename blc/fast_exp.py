#!/usr/bin/env python3

import requests
import time
import os
import argparse
import re
from lxml import html
from threading import Thread
import re
from datetime import datetime


def login(user, passw):
    global session

    if not (user or passw):
        return False

    loginLink = f"{baseUrl}/login/index.php"
    session.cookies.clear()
    loginPage = session.get(loginLink, headers=headers).text
    tree = html.fromstring(loginPage)
    logintoken = tree.xpath(
        "//form[@id='login']/input[@name='logintoken']")[0].value
    loginTry = session.post(loginLink, data={
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
    # print("")
    for i in range(s, 0, -1):
        print('-', end='', flush=True)
        time.sleep(1)
    # print("")


def sesskeyGet(allpageLink):
    return re.search(r"sesskey\"\:\"([^\"]+)", allpageLink, re.M).group(1)


def getAllEnrollCourse():
    allpageLink = session.get(f"{baseUrl}/my/", headers=headers).text
    sesskey = sesskeyGet(allpageLink)
    postUrl = fr"{baseUrl}/lib/ajax/service.php"

    data = session.post(
        postUrl,
        params={"sesskey": sesskey},
        json=[{"methodname": "core_course_get_enrolled_courses_by_timeline_classification",
               "args": {"classification": "all"}}], headers=headers).json()

    return data[0]["data"]["courses"]


def getLinks(courses):
    courseLink = []
    for link in courses:
        courseLink.append(link["viewurl"])
    return courseLink


def getSemister(semi=""):
    coursesGroup = courseGroup(getAllEnrollCourse())
    coursesGroupMarge = coursesGroup[0]
    coursesGroupMarge["unknown"] = coursesGroup[1]
    if not semi:
        coursesGrp = coursesGroup[0]
        coursesLevel = {
            "Summer": '1',
            "Spring": '0',
            "Fall": '2'
        }
        coursesLevelIndex = {
            '1': "Summer",
            '0': "Spring",
            '2': "Fall"
        }
        courseIndex = []
        for perSession, century in coursesGrp.items():
            for year in century.keys():
                courseIndex.append(int(f"{year}{coursesLevel[perSession]}"))

        courseLatest = str(sorted(courseIndex, reverse=True)[0])
        semi = f"{coursesLevelIndex[courseLatest[-1]]}{courseLatest[:2]}"
    print(semi, flush=True)
    return coursesGroupMarge[semi[:-2]][semi[-2:]]


def courseGroup(courses):
    coursesGroup = {
        "Summer": {},
        "Spring": {},
        "Fall": {}
    }

    coursesUnknown = {}

    for course in courses:
        brkFlag = False
        for perSession in coursesGroup:
            for section in ["coursecategory", "fullname", "fullnamedisplay"]:
                search = re.search(
                    perSession+".(\d{2,4})", course[section], re.IGNORECASE)
                if search:
                    try:
                        coursesGroup[perSession][
                            search.group(1)[-2:]].append(course)
                    except KeyError:
                        coursesGroup[perSession][
                            search.group(1)[-2:]] = [course]
                    brkFlag = True
                    break
                elif perSession == "unknown" and search == None:
                    century = datetime.utcfromtimestamp(
                        course['startdate']).strftime('%C')
                    try:
                        coursesUnknown[century].append(course)
                    except KeyError:
                        coursesUnknown[century] = [course]
                    break
            if brkFlag:
                break

    return (coursesGroup, coursesUnknown)


def marksAsDone(allpageLink):
    tree = html.fromstring(allpageLink)
    sesskey = sesskeyGet(allpageLink)
    postUrl = fr"{baseUrl}/lib/ajax/service.php"

    cmids = tree.xpath(
        "//button[@data-action='toggle-manual-completion' and @data-toggletype='manual:mark-done']/@data-cmid")
    if cmids:
        for cmid in cmids:
            print(cmid, "->", session.post(
                postUrl,
                params={"sesskey": sesskey},
                json=[{"methodname": "core_completion_update_activity_completion_status_manually",
                  "args":
                      {"cmid": int(cmid),
                       "completed": True}
                       }], headers=headers).json()[0]['data']["status"], flush=True)
    else:
        print("All Marks already Done", flush=True)


def loginCheck():
    faildCheck = False
    if args.m:
        try:
            allpageLink = session.get(baseUrl+"/my", headers=headers).text
            tree = html.fromstring(allpageLink)
            if not tree.xpath("//span[@class='username pr-1']"):
                raise Exception("404")
            return True
        except:
            faildCheck = True

    if faildCheck or (not args.m):
        if login(args.u, args.p):
            return True
        else:
            return False


def job(l):
    eT = 0
    old = 0

    clickLink = []

    allpageLink = session.get(l, headers=headers).text
    tree = html.fromstring(allpageLink)

    print("\n"+tree.xpath("//h3[@class='page-title mb-0']")[0].text, flush=True)
    if args.mark:
        marksAsDone(allpageLink)
    clickLink.append(l)
    clickLink += tree.xpath(
        "//div[@class='activityinstance']/a[@class='aalink']/@href")
    for ids, link in enumerate(clickLink):
        loop = ids
        try:
            trying = session.get(link, headers=headers, timeout=30, stream=True)
        except requests.exceptions.ReadTimeout as e:
            print(f"Timeout : {link}\nerror:{e}", flush=True)
            continue
        except requests.exceptions.ConnectionError as e:
            print(f"Timeout : {link}\nerror:{e}", flush=True)
            continue
        if not trying.status_code == 200:
            if eT < 3:
                print(f"Retrying... {eT}", flush=True)
                eT += 1
                continue
            else:
                clear_output()
                raise Exception(
                    f"Status code: {trying.status_code}\n count: {loop}\nLink: {link}")
        if ids == 0:
            tree = html.fromstring(trying.text)
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
                f"{name} xp:{nowEx-old if loop != 0 else 0}+ T:{nowEx}xp Loop:{loop} \n[0]", end='', flush=True)
            if loop != 0 and (nowEx-old) == 0:
                sleep(5)

            old = nowEx

        else:
            print(f"[{ids}]", end='', flush=True)
        sleep(5)


if __name__ == "__main__":
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
    parser.add_argument('--all', action=argparse.BooleanOptionalAction,
                        help='Work with all courses, without this flag auto get latest semister')
    parser.add_argument('--semi', type=str,
                        help='Define which semister with working ex: --semi Fall21')
    args = parser.parse_args()

    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.46 Safari/537.36',
    }

    baseUrl = "https://elearn.daffodilvarsity.edu.bd"

    jar = requests.cookies.RequestsCookieJar()
    jar.set('MoodleSession', args.m)

    session = requests.Session()
    session.cookies = jar

    if loginCheck():
        if not args.c:
            if args.all:
                courseLink = getLinks(getAllEnrollCourse())
            elif args.semi:
                courseLink = getLinks(getSemister(args.semi))
            else:
                courseLink = getLinks(getSemister())

            # print("courses>>", len(courseLink))
            # exit()
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
    else:
        raise Exception("Login unsccessful!")

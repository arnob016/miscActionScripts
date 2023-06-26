import re
import os
import requests
import simplejson
import json

def rawDataFIds():
    with open("rawData.txt", "r") as r:
        getIdList = re.findall(
            r"(\w.+)\s(\d{3}\-\d{2}\-\d{3,5})", r.read(), re.M)
    return getIdList


def sortData(data):
    return dict(sorted(data.items(), key=lambda item: data[item[0]]['sgpa'], reverse=True))


def cgpakeys(dic):
    for _, v in dic.items():
        return v['sgpa']


def readResult():
    if os.path.exists(saveFileName):
        with open(saveFileName, "r") as r:
            data = json.load(r)
        return data
    else:
        return {}


def cleanResult(data: dict):
    d = data.copy()
    for k, v in d.items():
        try:
            _ = v['listin']
            data[k].pop('listin', None)
        except:
            del data[k]
    return data


def saveResult(data):
    with open(saveFileName, "w") as w:
        json.dump(
            sortData(
                data
            ),
            w,
            indent=4
        )


def clearLine(l=50):
    print("\r"+l*2*" ", flush=True, end="")


def fetchData(url, id):
    # http://software.diu.edu.bd:8189/result/semesterList
    return requests.get(url, params={"semesterId": 231, "studentId": id, "grecaptcha": None}, verify=False)


if __name__ == "__main__":
    saveFileName = "resultsSavedFall2022.json"
    url = "http://software.diu.edu.bd:8189/result"

    urlInfo = f'{url}/studentInfo'
    m = rawDataFIds()
    getIdList = list(set(m))
    realData = readResult()

    for _ in range(5):
        print(len(getIdList), end="-")

        for i, p in enumerate(getIdList):
            try:
                found = ""
                getReq = fetchData(url, p[1])

                stdInfo = fetchData(urlInfo, p[1])
                jsonData = getReq.json()
                stdName = stdInfo.json()['studentName']
                if stdName is None:
                    stdName = p[0]
                # print(jsonData)
                sgpa = 0.0
                cTitleNgLetter = []
                for course in jsonData:
                    foundcourse = f'{course["courseTitle"]} | {course["gradeLetter"]}'
                    found += f'{course["courseTitle"]}\t{course["gradeLetter"]}\n'
                    cTitleNgLetter.append(foundcourse)
                    try:
                        sgpa = float(course["cgpa"]) #typo in base api
                    except ValueError:
                        pass
                    except TypeError:
                        pass
                found += "\n"
                dataJson = {
                    "sgpa": sgpa,
                    "name": stdName,
                    "cTitleNgLetter": sorted(cTitleNgLetter, key=lambda x: x.lower())
                }
                realData[p[1]] = dataJson
                saveResult(realData)
                getIdList.pop(i)
                tailString = f"\n{stdName} | sgpa: {sgpa} \n"
                clearLine(len(stdName))
                print(tailString+found)

            # Hard coded #json.decoder.JSONDecodeError #simplejson.errors.JSONDecodeError:
            except simplejson.errors.JSONDecodeError:
                if p[1] in realData:
                    getIdList.pop(i)
                    clearLine(len(p[0]))
                    print(
                        f"\n{realData[p[1]]['name']} sgpa: {realData[p[1]]['sgpa']} \n")
                    for c in realData[p[1]]['cTitleNgLetter']:
                        print(c)
                print("\r"+p[0]+len(p[0])*" ", flush=True, end="")
            try:
                realData[p[1]]['listin'] = True
            except:
                pass
            # os.exit()
    saveResult(cleanResult(realData))
    clearLine()

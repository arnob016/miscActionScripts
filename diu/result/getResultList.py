import re, os, requests, simplejson, time, json

def rawDataFIds():
    with open("rawData.txt", "r") as r:
        getIdList = re.findall(r"(\w.+)\s(\d{3}\-\d{2}\-\d{4})", r.read(), re.M)
    return getIdList

def sortData(data):
    return dict(sorted(data.items(), key=lambda item: data[item[0]]['cgpa'], reverse=True))

def cgpakeys(dic):
    for _,v in dic.items():
        return v['cgpa']

def readResult():
    if os.path.exists("resultsSaved.json"):
        with open("resultsSaved.json", "r") as r:
            data = json.load(r)
        return data
    else:
        return {}

def saveResult(data):
    with open("resultsSaved.json", "w") as w:
        json.dump(sortData(data), w, indent=4)

def clearLine(l=50):
    print("\r"+l*2*" ", flush=True, end="")

def fetchData(url, id):
    return requests.get(url, params={"semesterId": 213, "studentId":id, "grecaptcha": None}, verify=False)

if __name__ == "__main__":
    url = "http://software.diu.edu.bd:8189/result"
    urlInfo = f'{url}/studentInfo'
    getIdList = rawDataFIds()
    realData = readResult()
    for _ in range(10):
        print(len(getIdList), end="-")
        
        for i,p in enumerate(getIdList):
            try:
                found = ""
                getReq = fetchData(url, p[1])
                
                stdInfo = fetchData(urlInfo, p[1])
                jsonData = getReq.json()
                stdName = stdInfo.json()['studentName']
                
                #print(jsonData)
                cgpa = 0.0
                cTitleNgLetter = []
                for course in jsonData:
                    space = (35-len(course["courseTitle"]))*" "
                    foundcourse = f'{course["courseTitle"]}{space}\t {course["gradeLetter"]} \n'
                    found += foundcourse
                    cTitleNgLetter.append(foundcourse)
                    try:
                        cgpa = float(course["cgpa"])
                    except ValueError:
                        pass
                    except TypeError:
                        pass
                found+= "\n"
                dataJson = {
                    "cgpa": cgpa,
                    "name": stdName,
                    "cTitleNgLetter": cTitleNgLetter
                }
                realData[p[1]] = dataJson
                saveResult(realData)
                getIdList.pop(i)
                tailString = f"\n{stdName} | cgpa: {cgpa} \n"
                clearLine(len(stdName))
                print(tailString+found)
                
            except simplejson.errors.JSONDecodeError: #Hard coded #json.decoder.JSONDecodeError #simplejson.errors.JSONDecodeError:
                if p[1] in realData:
                    getIdList.pop(i)
                    clearLine(len(p[0]))
                    print(f"\n{realData[p[1]]['name']} cgpa: {realData[p[1]]['cgpa']} \n")
                    for c in realData[p[1]]['cTitleNgLetter']:
                        print(c)
                print("\r"+p[0]+len(p[0])*" ", flush=True, end="")
            #os.exit()
    clearLine()

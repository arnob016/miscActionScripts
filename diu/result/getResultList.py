import re, os, requests, simplejson, time, json

def rawDataFIds():
    with open("rawData.txt", "r") as r:
        getIdList = re.findall(r"(\w.+)\s(\d{3}\-\d{2}\-\d{4})", r.read(), re.M)
    return getIdList

def readResult():
    if os.path.exists("resultsSaved.json"):
        with open("resultsSaved.json", "r") as r:
            data = json.load(r)
        return data
    else:
        return []

def saveResult(data):
    with open("resultsSaved.json", "w") as w:
        json.dump(data, w, indent=4)

def clearLine(l=50):
    print("\r"+l*2*" ", flush=True, end="")


if __name__ == "__main__":
    url = "http://software.diu.edu.bd:8189/result"
    getIdList = rawDataFIds()
    realData = readResult()
    for _ in range(10):
        print(len(getIdList), end="-")
        
        for i,p in enumerate(getIdList):
            try:
                found = ""
                getReq = requests.get(url, params={"semesterId": 213, "studentId":p[1], "grecaptcha": None}, verify=False)
                #print(getReq.headers)
                
                jsonData = getReq.json()
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
                    "name": p[0],
                    "cTitleNgLetter": cTitleNgLetter
                }
                realData.append({p[1]:dataJson})
                saveResult(realData)
                getIdList.pop(i)
                tailString = f"\n{p[0]} | cgpa: {cgpa} \n"
                clearLine(len(p[0]))
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

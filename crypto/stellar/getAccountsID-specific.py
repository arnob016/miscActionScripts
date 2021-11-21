import time, requests

def save_file(data):
  with open("accounts.txt", "a+") as w:
    for i in data:
      if i['type'] == 1:
        try:
          fount = "YBX-" in i["assets"][0]
        except KeyError:
          fount = False
        if fount:
          print(i['id'], end=" ")
          w.write(i['id']+" ")
          for acc in i['accounts']:
            print(acc, end=" ")
            w.write(acc+" ")
          print()
          w.write("\n") 

assetId = "YBX-GBUYYBXWCLT2MOSSHRFCKMEDFOVSCAXNIEW424GLN666OEXHAAWBDYMX-1"
tgUrl = f"https://api.stellar.expert/explorer/public/asset/{assetId}/history/all"
# https://stellar.expert/explorer/public/asset/

params={"limit": 200, "filter":"payments"}
getData = requests.get(tgUrl, params=params).json()['_embedded']['records']
# pp(getData)
# exit()
dataCount = len(getData)

count = 0
while dataCount!=0:
  save_file(getData)
  try:
    nowId = getData[-1]['id']
  except IndexError:
    print("Get: ", count, ":", dataCount, nowId)
    exit()
  print("Get: ", count, ":", dataCount, nowId)
  for p in range(10):
    try:
      params["cursor"] = nowId
      getData = requests.get(
          tgUrl,
          params=params
      ).json()['_embedded']['records']
      break
    except:
      print("Error")
      time.sleep(2)
  dataCount = len(getData)
  count+=1

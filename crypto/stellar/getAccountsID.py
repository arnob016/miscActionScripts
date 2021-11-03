import time

onlyAccounts = []
def save_file(data):
  with open("accounts.txt", "a+") as w:
    for i in data:
      id = i['accounts'][0]
      if (id not in onlyAccounts):
        w.write(i['accounts'][0]+"\n")
      onlyAccounts.append(id)

assetId = "YBX-GBUYYBXWCLT2MOSSHRFCKMEDFOVSCAXNIEW424GLN666OEXHAAWBDYMX"
tgUrl = f"https://api.stellar.expert/explorer/public/asset/{assetId}/history/all"

data = requests.get(tgUrl, params={"filter": "trustlines", "limit": 100, "order":"desc", "sort":"id"}).json()['_embedded']['records']
nowId = data[-1]['id']
preId = data[0]['id']
count = 0
while nowId!=preId:
  try:
    getDataR = requests.get(
        tgUrl,
        params={"limit": 200, "order":"desc", "sort":"id", "cursor": nowId}
    ).json()
    getData = getDataR['_embedded']['records']
  except:
    print("error")
    time.sleep(10)
    continue
  
  data.extend(getData)
  save_file(getData)
  preId = nowId
  nowId = getData[-1]['id']
  print("Get: ", len(data), ":", count, preId, nowId)
  count+=1

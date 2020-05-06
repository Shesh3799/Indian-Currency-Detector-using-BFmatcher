import json

with open('config.json') as f:
    data=json.load(f)
print(data['params']['login_page'])
data['params']['login_page']=0
print(data['params']['login_page'])

with open('config.json','w') as f:
    json.dump(data,f)
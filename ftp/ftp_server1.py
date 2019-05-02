

# import requests
# import json

# conn = requests.session()
# arcsearch="https://mbxcweb.hz.taeapp.com/app/#/titleOptimize/searchKeyword"

# ajax_header={'Authorization': 'Bearer symazkWo3mx5oycg+GEEjA=='}
# searchdata={'keyword': '人工智能'}
# # r = requests.get(url, headers=headers, data=searchdata)

# # print(r.status_code)
# # print(r.content)
# search = conn.post(arcsearch, data=searchdata, headers=ajax_header)
# print(search.json())





import requests
import json
 
url = "https://mbxcweb.hz.taeapp.com/_api/v2/industry-word/query"
body = {'keyword': '短款'}
headers = {'Authorization': 'Bearer symazkWo3mx5oycg+GEEjA=='}
 
#print type(body)
#print type(json.dumps(body))
# 这里有个细节，如果body需要json形式的话，需要做处理
# 可以是data = json.dumps(body)
response = requests.get(url, data = body, headers = headers)
# 也可以直接将data字段换成json字段，2.4.3版本之后支持
# response  = requests.post(url, json = body, headers = headers)
 
# 返回信息
# response.encoding="utf-8"
print((response.text)['message'])

# 返回响应头
#print(response.status_code)
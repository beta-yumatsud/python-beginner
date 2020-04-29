# XML
import xml.etree.ElementTree as ET

root = ET.Element('root')
tree = ET.ElementTree(element=root)
employee = ET.SubElement(root, 'employee')

employ = ET.SubElement(employee, 'employ')
employ_id = ET.SubElement(employ, 'id')
employ_id.text = '111'
employ_name = ET.SubElement(employ, 'name')
employ_name.text = 'Mike'

employ = ET.SubElement(employee, 'employ')
employ_id = ET.SubElement(employ, 'id')
employ_id.text = '222'
employ_name = ET.SubElement(employ, 'name')
employ_name.text = 'Nancy'

tree.write('dist/test.xml', encoding='utf-8', xml_declaration=True)

tree = ET.ElementTree(file='dist/test.xml')
root = tree.getroot()

for employee in root:
    for employ in employee:
        for person in employ:
            print(person.tag, person.text)

# Json
import json

j = {
    "employee": [
        {
            "id": 111,
            "name": "Mike"
        },
        {
            "id": 222,
            "name": "Nancy"
        }
    ]
}
print(j)
print("#####")
result = json.dumps(j)
print(result)

print('@@@@@@@@@')
print(json.loads(result))

with open('dist/test.json', 'w') as f:
    json.dump(j, f)

with open('dist/test.json', 'r') as f:
    print(json.load(f))
print('|||||||||||||')

# urllib.request
import urllib.request

# GET
payload = {'key1': 'value1', 'key2': 'value2'}

url = 'http://httpbin.org/get' + '?' + urllib.parse.urlencode(payload)
with urllib.request.urlopen(url) as f:
    r = json.loads(f.read().decode('utf-8'))
    print(r)

# POST
# PUTはmethodをPUTに、DELETEはmethodをDELETEにすればOK
payload = json.dumps(payload).encode('utf-8')
req = urllib.request.Request('http://httpbin.org/post', data=payload, method='POST')

with urllib.request.urlopen(req) as f:
    print(json.loads(f.read().decode('utf-8')))

print("~~~~~~~~~~~~~")

# requests(3rd party)
# $ pip install requests
import requests

# GET
r = requests.get('http://httpbin.org/get', params=payload, timeout=5)
print(r.status_code)
print(r.text)
print(r.json())

# POST(PUT, DELETEも呼び出すメソッドを変えればOK)
r = requests.post('http://httpbin.org/post', data=payload)
print(r.status_code)
print(r.text)
print(r.json())


# HTTP SERVER
# import http.server
# import socketserver

# OSSのWebフレームワーク内部的で下記のようなものを使っているよー
# with socketserver.TCPServer(('127.0.0.1', 8000),
#                             http.server.SimpleHTTPRequestHandler) as httpd:
#     httpd.serve_forever()

# BeautifulSoupでWebスクレイピング
from bs4 import BeautifulSoup

html = requests.get('https://www.python.org')
soup = BeautifulSoup(html.text, features="html.parser")

titles = soup.find_all('title')
print(titles)
print(titles[0].text)

intro = soup.find_all('div', {'class': 'introduction'})
print(intro[0].text)

# XML RPC
# 別ファイル
# 他にも Json RPCもあるみたい

# networkx
# https://networkx.github.io/documentation/stable/tutorial.html
# $ pip install networkx
# $ pip install matplotlib
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_node(1)

G.add_nodes_from([2, 3])

G.add_edge(1, 2)
G.add_edge(2, 3)
nx.draw(G)
plt.show()

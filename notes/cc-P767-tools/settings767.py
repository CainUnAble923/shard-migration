import json, shutil
p = r'D:\UO\golem\settings.json'
shutil.copy2(p, p + '.bak-20261101-P767')
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
s = raw.replace('\r\n', '\n')
old = '''                              "lane-chase":  [
                                                 "C:\\\\Users\\\\ckfle\\\\.codex"
                                             ]
                          },'''
new = '''                              "lane-chase":  [
                                                 "C:\\\\Users\\\\ckfle\\\\.codex"
                                             ],
                              "lane-steph":  [
                                                 "D:\\\\UO\\\\golem\\\\codex-home\\\\lane-steph"
                                             ]
                          },'''
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
json.loads(s)  # still valid
tmp = p + '.new-P767'
open(tmp, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
import os
os.replace(tmp, p)
print(json.dumps(json.loads(open(p, encoding='utf-8').read())['codexAccountHomes']))

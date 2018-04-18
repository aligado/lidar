#! usr/bin/python
# coding=utf-8 

import json
msg1 = [{'src':123, 'dst':"zjdst"}, {'src':456, 'dst':"zjdst"}]
print msg1[0]
print msg1[0]['src']
jmsg1 = json.dumps(msg1)
msg2 = json.loads(jmsg1.encode('utf-8'))
print jmsg1[0]
print jmsg1
msg2[1]['dst'] = msg2[1]['dst'].encode('utf-8')
print msg2[1]

print msg2[0]['src'] + msg2[1]['src']

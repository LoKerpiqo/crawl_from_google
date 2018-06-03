import os
import time


file = open("/Users/wuxinheng/Documents/CUB_200_2011/CUB_200_2011/class30_47.txt", "r")
queries = file.read().split('\n')
query=list()
for q in queries:
    query.append(q.split('.')[-1])

for q in query:
    time.sleep(1)
    n=1000
    cmd = 'python soup.py %s %d' % (q, n)
    os.system(cmd)
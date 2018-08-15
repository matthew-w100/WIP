import time

t=time.clock()
time.sleep(3)
t=(time.clock()-t)
print(t)
print(time.asctime(time.gmtime(t)))
print(time.asctime(time.localtime()))


      



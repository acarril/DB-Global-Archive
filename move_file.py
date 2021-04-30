import os
import shutil
import sys
import time

file_in = sys.argv[1]
file_out = sys.argv[2]

while not os.path.isfile(file_in):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) ,'source file not found')
    time.sleep(3600)

shutil.move(file_in, file_out)
print(file_in, '-->', file_out)
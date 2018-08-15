import os
calibre_path = os.path.join('d:\\', 'media', 'calibretest')
print(calibre_path)
pwd = os.getcwd()
print(pwd)
os.chdir(calibre_path)
pwd = os.getcwd()
print(pwd)
dirCalibre = os.listdir(calibre_path)
for file in dirCalibre:
    size = os.path.getsize(os.path.join(calibre_path,file))
    print(size, ' ', file)

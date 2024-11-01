import zipfile
import shutil
import os
import ebooklib
from ebooklib import epub

bookName = '転生王女と天才令嬢の魔法革命【Web版】'

os.makedirs('tmp')
zip_ref = zipfile.ZipFile(bookName+'.epub')
zip_ref.extractall('./tmp')

file = open('./tmp/EPUB/nav.xhtml','r',encoding='utf-8')
originText = file.read()
newText = originText.replace('<ol>','<ul>')
newText = newText.replace('</ol>','</ul>')
file.close()

file = open('./tmp/EPUB/nav.xhtml','w',encoding='utf-8')
file.write(newText)
file.close()
###################
def dfs(path,zf):
    for root, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(root,file)
            newpath = filePath.replace('./tmp\\','.\\')
            #print(os.path.join(root, file))
            zf.write(filePath,newpath)

reZip = zipfile.ZipFile('test.zip','w')
dfs('./tmp',reZip)
reZip.close()

os.rename('test.zip',bookName+'_v2.epub')

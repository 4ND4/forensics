import pytsk3
import os
import hashlib

listObject = []
listSHA1 = []
listDuplicate = []

print os.name

def directoryRecurse(directoryObject, parentPath):
    for entryObject in directoryObject:
        if entryObject.info.name.name in [".", ".."]:
            continue

        try:
            f_type = entryObject.info.meta.type
        except:
            print "Cannot retrieve type of", entryObject.info.name.name
            continue

        try:

            filePath = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name)

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entryObject.as_directory()
                parentPath.append(entryObject.info.name.name)
                directoryRecurse(sub_directory, parentPath)
                parentPath.pop(-1)
                print "Directory: %s" % filePath

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:

                fileData = entryObject.read_random(0, entryObject.info.meta.size)

                md5hash = hashlib.md5()
                md5hash.update(fileData)
                sha1hash = hashlib.sha1()
                sha1hash.update(fileData)
                listObject.append(entryObject)

                listSHA1.append(md5hash.hexdigest())

        except IOError as e:
            print e
            continue

imageFile = open(os.path.expanduser("D:/Forensics/shaCollision.001"))

url = imageFile.name

dirPath = "/"

imageHandle = pytsk3.Img_Info(url)

#determine partition type

partitionTable = pytsk3.Volume_Info(imageHandle)

for partition in partitionTable:
    if 'FAT32' in partition.desc:
        filesystemObject = pytsk3.FS_Info(imageHandle, offset=(partition.start*512))  # absolute offset 512
        directoryObject = filesystemObject.open_dir(path=dirPath)

        directoryRecurse(directoryObject, [])

for i in range(len(listSHA1)):
    for j in range(i+1, len(listSHA1)):

        if listSHA1[i] == listSHA1[j]:
            if i not in listDuplicate:
                listDuplicate.append(i)
            if j not in listDuplicate:
                listDuplicate.append(j)

for i in listDuplicate:
    if listObject[i].info.meta.size != 4096:        # find out a better filter for empty directories
        output = open(listObject[i].info.name.name, "w+")
        output.write(listObject[i].read_random(0, listObject[i].info.meta.size))
        output.close
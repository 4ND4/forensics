import pytsk3
import os
import hashlib

list = []

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

            filepath = '/%s/%s' % ('/'.join(parentPath), entryObject.info.name.name)

            if f_type == pytsk3.TSK_FS_META_TYPE_DIR:
                sub_directory = entryObject.as_directory()
                parentPath.append(entryObject.info.name.name)
                directoryRecurse(sub_directory, parentPath)
                parentPath.pop(-1)
                print "Directory: %s" % filepath

            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size != 0:

                filedata = entryObject.read_random(0, entryObject.info.meta.size)
                md5hash = hashlib.md5()
                md5hash.update(filedata)
                sha1hash = hashlib.sha1()
                sha1hash.update(filedata)

                list.append(filedata)

                print entryObject.info.name.name
                print md5hash.hexdigest()


            elif f_type == pytsk3.TSK_FS_META_TYPE_REG and entryObject.info.meta.size == 0:

                '''
                wr.writerow([int(entryObject.info.meta.addr), '/'.join(parentPath) + entryObject.info.name.name,
                             datetime.datetime.fromtimestamp(entryObject.info.meta.crtime).strftime(
                                 '%Y-%m-%d %H:%M:%S'), int(entryObject.info.meta.size),
                             "d41d8cd98f00b204e9800998ecf8427e", "da39a3ee5e6b4b0d3255bfef95601890afd80709"])
                '''

        except IOError as e:
            print e
            continue

imageFile = open(os.path.expanduser("~/Documents/UCD/Work/AssignmentImage.dmg"))

url = imageFile.name

dirPath = "/"

# img = pytsk3.Img_Info(url)

# imageFile = r"/././dev/disk2"   # diskutil list  live forensics

# imageHandle = pytsk3.Img_Info(imageFile)

imageHandle = pytsk3.Img_Info(url)

partitionTable = pytsk3.Volume_Info(imageHandle)

for partition in partitionTable:
    #print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len

    if 'FAT32' in partition.desc:
        filesystemObject = pytsk3.FS_Info(imageHandle, offset=(partition.start*512))  # absolute offset 512
        directoryObject = filesystemObject.open_dir(path=dirPath)

        #print "Directory: ", dirPath

        directoryRecurse(directoryObject, [])
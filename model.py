import pytsk3


class DiskImage:
    def __init__(self, file_path):
        self.id=1
        self.size=20
        self.name="Forensic Image"
        self.type = "FAT16"
        self.os = "WINDOWS"
        self.file_path = file_path


class Partition:
    def __init__(self, address, description, start, length):
        self.address = address
        self.description = description
        self.start = start
        self.offset = self.start * 512
        self.length = length

    def get_partitions(self):
        partitions = []

        with open(self.file_path) as imageFile:
            image_handle = pytsk3.Img_Info(imageFile.name)

        partition_table = pytsk3.Volume_Info(image_handle)

        for partition in partition_table:
            #print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
            partitions.add(Partition(partition.addr, partition.desc, partition.start, partition.len))
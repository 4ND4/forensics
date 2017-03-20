import model


class View():

    def list_partition(self):
        print model.Partition.addr, model.Partition.desc, "%ss(%s)" % (model.Partition.start, model.Partition.offset), model.Partition.len
import pytsk3


def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

if __name__ == "__main__":
    import argparse, os
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Image processing")
    parser.add_argument(
        "-i",
        "--input",
        dest="filename",
        required=True,
        type=extant_file,
        help="input image path",
        metavar="FILE"
    )

    args = parser.parse_args()

    with open(args.filename) as imageFile:
        imageHandle = pytsk3.Img_Info(imageFile.name)

    partitionTable = pytsk3.Volume_Info(imageHandle)

    for partition in partitionTable:
        print partition.addr, partition.desc, "%ss(%s)" % (partition.start, partition.start * 512), partition.len
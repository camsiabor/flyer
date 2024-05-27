from scripts import util

if __name__ == '__main__':

    def callback(file1, file2):
        if file1 is not None:
            print(file1)
        if file2 is not None:
            print(file2)
        print("======")


    src_dir = "D:/novel"
    des_dir = "D:/output"
    """
    util.FileIO.walk(
        src_dir,
        callback_file=callback,
        file_ext=".txt",
        depth_limit=3
    )
    """

    util.FileIO.walk_des(
        src_dir=src_dir,
        des_dir=des_dir,
        callback_dir=None,
        callback_file=callback,
        depth_limit=3
    )

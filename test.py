from scripts.service import text_process

if __name__ == '__main__':
    src_file = "D:/novel/cthulhu/lord_of_mystery.txt"
    des_dir = "D:/novel/cthulhu/output"

    text_process.split_file(
        src_file=src_file,
        des_dir=des_dir,
    )

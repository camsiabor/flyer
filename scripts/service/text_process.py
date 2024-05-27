def to_utf8(src_file, des_file):
    with open(src_file, "r", encoding="utf-8") as source:
        content = source.read()
        with open(des_file, "w", encoding="utf-8") as target:
            target.write(content)

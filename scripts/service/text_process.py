import chardet


def to_utf8(src_file, des_file, buffer_size=512 * 1024):
    if isinstance(buffer_size, str):
        buffer_size = eval(buffer_size)

    # Detect the source file encoding
    with open(src_file, 'rb') as source:
        rawdata = source.read(1024)
        result = chardet.detect(rawdata)
        source_encoding = result['encoding']

    # Read the source file with the detected encoding and write to the destination file in utf-8
    with open(src_file, "r", encoding=source_encoding) as source:
        with open(des_file, "w", encoding="utf-8") as target:
            while True:
                chunk = source.read(buffer_size)
                if not chunk:
                    break
                target.write(chunk)

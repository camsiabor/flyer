import os

import chardet


def to_utf8(src_file, des_file, buffer_size=512 * 1024):
    if isinstance(buffer_size, str):
        buffer_size = eval(buffer_size)

    # Detect the source file encoding
    with open(src_file, 'rb') as source:
        rawdata = source.read(512)
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


def split_file(
        src_file, des_dir,
        encoding='utf-8',
        prefix="", suffix=".txt",
        padding=6
):
    os.makedirs(des_dir, exist_ok=True)

    if prefix is None or prefix == "":
        prefix = os.path.splitext(os.path.basename(src_file))[0] + "_"

    with open(src_file, mode='r', encoding=encoding) as file:
        content = file.read()
        chapters = content.split('\n\n')  # Split by double new lines

    for i, chapter in enumerate(chapters):
        # Pad the chapter number with zeros
        padded_chapter_num = str(i + 1).zfill(padding)
        output_file_path = os.path.join(des_dir, f'{prefix}{padded_chapter_num}{suffix}')
        with open(output_file_path, 'w', encoding=encoding) as file:
            file.write(chapter)

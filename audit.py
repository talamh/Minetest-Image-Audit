import os
import zlib
import zipfile
from json import JSONDecodeError
from json import loads
import argparse


def traverse(base_dir: str, ext: str) -> list:
    """
    Recursively traverse a directory to find all files ith a given extension
    :param base_dir: starting directory
    :param ext: extension of files of interest
    :return:
    """
    image_list = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(f"{ext}"):
                image_list.append(os.path.join(root, file))

    return image_list


def check_duplicates(images: list) -> None:
    """

    Check all image crcs against each other to check for duplicates

    :param images: images to check
    :return: None
    """

    processed = {}
    print('Duplicate Check:')

    for i in images:
        with open(i, "rb") as img:
            crc = zlib.crc32(img.read())
            if crc in processed:
                updated_value = processed.pop(crc)
                updated_value.append(i)
                processed[crc] = updated_value
            else:
                processed[crc] = [i]

    for i in processed:
        if len(processed.get(i)) > 1:
            print(f'crc: {i} : {len(processed.get(i))} files:')
            for curr_image in processed.get(i):
                print(f'\t{curr_image}')


def check_plagiarism(images: list) -> None:
    """
    check all images against Minecraft crcs to check for copyright infringing images
    :param images: images to check
    :return: None
    """

    minecraft_formats = ['1.8.9', '1.10.2', '1.12.2', '1.14.4',
                         '1.16.1', '1.16.5', '1.17.1', '1.18.2']

    print('\nMinecraft check:')

    try:
        with zipfile.ZipFile(f'{"./crcs/minecraft_crcs.zip"}', 'r') as archive:
            try:
                minecraft_crc = loads(archive.read('crcs.json').decode('utf-8'))
            except (KeyError, JSONDecodeError) as error:
                print(f'failed to read minecraft_crcs.zip: {error}')
                return
    except FileNotFoundError as error:
        print(f'failed to open minecraft_crcs.zip: {error}')
        return

    from_minecraft = 0
    for i in images:
        with open(i, "rb") as img:
            crc = zlib.crc32(img.read())
            if str(crc) in minecraft_crc:
                from_minecraft += 1
                mc_image = minecraft_crc.get(str(crc))
                print(f'image file {i} is identical to:')
                for mci in mc_image:
                    print(f'\t{mci[0]} in Minecraft {minecraft_formats[mci[1] - 1]}')

    print(f'Minecraft images {from_minecraft} out of {len(images)}')


def main():
    parser = argparse.ArgumentParser(description="Minetest image auditor.")
    parser.add_argument("-i", help="Starting directory", required=True)
    args = parser.parse_args()

    images = traverse(args.i, 'png')
    check_duplicates(images)
    check_plagiarism(images)


if __name__ == "__main__":
    main()

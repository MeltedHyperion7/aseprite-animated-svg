import xml.dom.minidom as md
import os
import argparse
import re

from Frame import Frame

def is_file(string):
    """ Ensure that the path entered is a real file. """

    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)

parser = argparse.ArgumentParser()
parser.add_argument('path', type=is_file)

def get_file_list(dirname, file_name_without_number):
    """ Returns the list of all svg files in the animation. """

    all_files = os.listdir(dirname)
    number = 1
    animation_files = []

    while True:
        file_name = f'{file_name_without_number}{number}.svg'

        if file_name not in all_files:
            return animation_files

        animation_files.append(f'{dirname}/{file_name}')
        number += 1

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        dirname = os.path.dirname(args.path)
        basename = os.path.basename(args.path)
        file_name, file_extension = basename[:-4], basename[-4:]
        file_match = re.search('\w(\d+).svg$', basename)

        if file_match is None:
            # ensure that the file meets the naming conventions
            raise FileNotFoundError

        # prepare a list of all svg files we need to process
        number = file_match.groups()[0]
        file_name_without_number = file_name[:-len(number)]
        files = get_file_list(dirname, file_name_without_number)

        num_frames = len(files)
        frames = [Frame(file) for file in files]

    except FileNotFoundError:
        print('Provide a valid SVG file.')

#!/usr/bin/env python

# Create a release package for Draker's products

import shutil
import argparse

def copyFile(src, dest):
    try:
        shutil.copy2(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

def importfilelist():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', 'source_folder', help='defines the source directories to copy from')
    parser.add_argument('dest', 'dest_folder', help='defines the destination folder to copy to')
    parser.add_argument('-lof', '--list-of-files', help='defines the file that constains the list of files to use to create the release package', default='')
    args = parser.parse_args()
    main()
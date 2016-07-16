#!/usr/local/bin/python
# -*- coding: utf-8 -*-

TEXT_ENCODING = 'utf8'

# General libraries
import argparse, fnmatch, glob, os, re, sys

# Mutagen (for processing MP3 files)
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# Global variables
DEBUG = False


def main():
    global DEBUG

    parser = argparse.ArgumentParser(description='Finds MP3 files within the specified filesystem path and generates a PDF song list grouped by artist')
    parser.add_argument('-d', '--debug',  required=False, default=False, action='store_true', help='enable debug mode', )
    parser.add_argument('-c', '--clean',  required=False, default=False, action='store_true', help='cleans all ID3 data and sets only artist/song', )
    parser.add_argument('-p', '--path',   required=False, default='.',   help='path to search for MP3 files', )
    args = parser.parse_args()

    DEBUG       = args.debug
    clean       = args.clean
    path        = args.path

    if DEBUG:
        print 'Debug mode enabled'

    # Search for songs
    print 'Searching for files in: {}'.format(path)

    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            filepath = os.path.join(root, filename)
            print 'Processing {}...'.format(filepath)


            pattern = re.compile('\.mp3$', re.IGNORECASE)
            filename = pattern.sub('', filename)

            artist, title = filename.split(' - ', 1)

            if DEBUG:
                print '\tLoading...'

            mp3 = MP3(filepath, ID3=EasyID3)

            try:
                # Remove all tags if clean is set
                if clean:
                    if DEBUG:
                        print '\tClearing existing tags'

                    mp3.delete()

                # Set the artist and song title
                mp3['artist'] = artist
                mp3['title']  = title

                if DEBUG:
                    print '\tSaving...'

                # Saving V1 for backward compatibility with certain software
                mp3.save(v1=2)

            except:
                print 'Error resetting tags for file {}'.format(filepath)
                return


if __name__ == "__main__":
    main()

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

TEXT_ENCODING = 'utf8'

# General libraries
import argparse, fnmatch, os
from sets import Set

# Mutagen (for processing MP3 files)
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# Reportlab (for generating the PDF song list)
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, PageTemplate, NextPageTemplate, Table, TableStyle
from reportlab.lib import pagesizes, colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Template additions to customize how pages are rendered
import template

# Global variables
DEBUG = False

library = []
artists = Set()

sectionList    = []
sectionIter    = iter(sectionList)
currentSection = ''

headerTextTemplate = ''
footerTextTemplate = ''

def main():
    global DEBUG
    global library, artists
    global sectionList, sectionIter, currentSection
    global headerTextTemplate, footerTextTemplate

    parser = argparse.ArgumentParser(description='Finds MP3 files within the specified filesystem path and generates a PDF song list grouped by artist')
    parser.add_argument('-d', '--debug',  required=False, default=False, action='store_true', help='Enable debug mode')
    parser.add_argument('-p', '--path',   required=False, default='.', help='Path to search for MP3 files')
    parser.add_argument('-o', '--output', required=False, default='SongList.pdf', help='Output filename')
    parser.add_argument('-t', '--title',  required=False, default='Karaoke Songs by Artist ({})', help='Header and footer title per page')
    args = parser.parse_args()

    DEBUG       = args.debug
    path        = args.path
    output_file = args.output
    headerTextTemplate = args.title
    footerTextTemplate = args.title

    if DEBUG:
        print 'Debug mode enabled'

    # Search for songs
    print 'Searching for files in: {}'.format(path)
    discover(path)
    print 'Found {} songs for {} artists'.format(len(library), len(artists))

    # If we don't have any songs or any artists indexed, then just return
    if (len(library) == 0 or len(artists) == 0):
        print 'Skipping PDF generation'
        return

    # Need to generate sections based upon the artist
    for artist in sorted(artists):
        # Pre-populate the various sections
        section = getSection(artist)

        if (sectionList[-1:] != [section]):
            sectionList.append(section)

        # Print out each song found if in debug mode
        if DEBUG:
            songs = [entry['title'] for entry in library if entry['artist'] in [artist]]

            print u'\n{}'.format(artist)

            for song in sorted(songs):
                print u'\t{}'.format(song)

            print '\n'

    sectionIter = iter(sectionList)
    currentSection = next(sectionIter)

    print 'Generating PDF: {}'.format(output_file)
    generatePdf(output_file)


def discover(path):
    global library
    global artists

    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            filepath = os.path.join(root, filename)

            metadata = getMetadataFromFile(filepath)

            entry = {
                'path':   filepath,
                'artist': metadata['artist'],
                'title':  metadata['title']
            }

            library.append(entry)
            artists.add(entry['artist'])


def getMetadataFromFile(f):
    if DEBUG:
        print "Processing file '{}...'".format(f)

    m = MP3(f, ID3=EasyID3)

    return {
        'path': f,
        'artist': m['artist'][0],
        'title': m['title'][0]
    }


def updateFlowableData(flowable):
    global currentSection, sectionIter

    if (hasattr(flowable, 'newSection')):
        currentSection = next(sectionIter)


def getSection(artist):
    if ('0' < artist[0] < '9'):
        return '#'
    else:
        return artist[0].upper()


def setCustomPageData(canvas, doc):
    global currentSection
    global headerTextTemplate, footerTextTemplate

    canvas._currentHeaderText = headerTextTemplate.format(currentSection)
    canvas._currentFooterText = footerTextTemplate.format(currentSection)


def generatePdf(filename):
    if (DEBUG):
        sb = 1
    else:
        sb = 0

    doc = BaseDocTemplate(
                      filename,
                      pagesize     = pagesizes.letter,
                      leftMargin   = 0.25*inch,
                      rightMargin  = 0.25*inch,
                      topMargin    = 0.25*inch,
                      bottomMargin = 0.25*inch,
                      showBoundary = sb)

    left_col1Frame = Frame(
                      doc.leftMargin   + 0.75*inch,
                      doc.bottomMargin + 0.15*inch,
                      doc.width/2      - 0.50*inch,
                      doc.height       - 0.15*inch,

                      leftPadding   = 0.00,
                      rightPadding  = 0.00,
                      topPadding    = 0.75*inch,
                      bottomPadding = 0.25*inch,

                      showBoundary  = sb,
                      id = 'Left_Column1Frame')

    left_col2Frame = Frame(
                      doc.leftMargin   + doc.width/2 + 0.50*inch,
                      doc.bottomMargin + 0.15*inch,
                      doc.width/2      - 0.50*inch,
                      doc.height       - 0.15*inch,

                      leftPadding   = 0.00,
                      rightPadding  = 0.00,
                      topPadding    = 0.75*inch,
                      bottomPadding = 0.25*inch,

                      showBoundary  = sb,
                      id = 'Left_Column2Frame')

    right_col1Frame = Frame(
                      doc.leftMargin   + 0.00*inch,
                      doc.bottomMargin + 0.15*inch,
                      doc.width/2      - 0.50*inch,
                      doc.height       - 0.15*inch,

                      leftPadding   = 0.00,
                      rightPadding  = 0.00,
                      topPadding    = 0.75*inch,
                      bottomPadding = 0.25*inch,

                      showBoundary  = sb,
                      id = 'Right_Column1Frame')

    right_col2Frame = Frame(
                      doc.leftMargin   + doc.width/2 - 0.25*inch,
                      doc.bottomMargin + 0.15*inch,
                      doc.width/2      - 0.50*inch,
                      doc.height       - 0.15*inch,

                      leftPadding   = 0.00,
                      rightPadding  = 0.00,
                      topPadding    = 0.75*inch,
                      bottomPadding = 0.25*inch,

                      showBoundary  = sb,
                      id = 'Right_Column2Frame')


    doc.addPageTemplates([PageTemplate(
                          id='pageLeft',
                          frames=[left_col1Frame, left_col2Frame],
                          onPage=setCustomPageData
                        )])

    doc.addPageTemplates([PageTemplate(
                          id='pageRight',
                          frames=[right_col1Frame, right_col2Frame],
                          onPage=setCustomPageData
                        )])

    doc.afterFlowable = updateFlowableData

    Elements = []

    # this will cycle through right/left/right/left
    Elements.append(NextPageTemplate(['pageRight', 'pageLeft']))

    # this will cycle through first/second/left/right/left/right/...
    # Elements.append(NextPageTemplate(['firstPage', 'secondPage', '*', 'pageLeft', 'pageRight']))

    tableStyle = TableStyle([('FONT',       (0,0), (-1, 0), 'Helvetica-Bold', 9),
                             ('BACKGROUND', (0,0), (-1, 0), colors.CMYKColor(0, 0, 0, 0.1)),
                             ('FONT',       (0,1), (-1,-1), 'Helvetica', 9),
                             ('TEXTCOLOR',  (0,0), (-1,-1), colors.black),
                             ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
                             ('LINEBELOW',  (0,0), (-1,-2), 0.5, colors.CMYKColor(0, 0, 0, 0.50)),
                             ('LINEABOVE',  (0,0), (-1, 0), 0.5, colors.CMYKColor(0, 0, 0, 0.50)),
                            ])

    lastSection = False

    for artist in sorted(artists):
        currentSection = getSection(artist)

        if (currentSection != lastSection):
            if (lastSection):
                Elements.append(PageBreak())
                Elements[-1].newSection = True

            lastSection = currentSection

        data = []
        data.append([artist])

        for song in sorted([entry['title'] for entry in library if entry['artist'] in [artist]]):
            data.append([song])

        songTable = Table(data, ['*'], repeatRows=1)
        songTable.setStyle(tableStyle)

        Elements.append(songTable)

    # Use the custom template canvas
    doc.build(Elements, canvasmaker=template.Canvas)


if __name__ == "__main__":
    main()

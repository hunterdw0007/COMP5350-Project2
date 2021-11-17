# Hunter Westerlund and Charlotte Vance
# COMP 5350 Project 2

# References
# https://www.reddit.com/r/learnpython/comments/6m7ptm/find_hexadecimal_offset_of_certain_bytes_in/
# https://stackoverflow.com/questions/27001419/how-to-append-to-bytes-in-python-3
# https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
# https://www.geeksforgeeks.org/file-handling-python/
# https://id3.org/id3v2.3.0

#imports
import sys
import os
import struct

# this is where the name of the disk image will come in
filename = sys.argv[1]
#filename = 'Project2.dd'

#finding the size of the disk image for later use
image_size = os.path.getsize(filename)

#MPG
def MPGRecovery():
    print('\nMPG File locations:')
    with open(filename, 'rb') as f:
        s = f.read()

        # ID3 MP3
        print('\nID3 MP3:')
        try:
            index = 0
            while True:
                index = s.index('\x49\x44\x33', index)
                print('Start Offset: ' + hex(index))
                f.seek(index + 6, 0)
                filesize = f.read(4)
                # TODO Upgrade to Python 3
                filesizeint = int.from_bytes(filesize, "big")
                print('Filesize: ' + hex(filesizeint))
                index += 3
        except ValueError:
            print("EOF")

        # M4A
        print('\nM4A')
        try:
            index = 0
            while True:
                index = s.index('\x66\x74\x79\x70\x4D\x34\x41\x20', index)
                print('Start Offset: ' + hex(index - 4))
                index += 8
        except ValueError:
            print("EOF")

        # CD MPEG-1
        print('\nCD MPEG-1:')
        try:
            index = 0
            while True:
                index = s.index('\x52\x49\x46\x46', index)
                print('Start Offset: ' + hex(index))
                index += 4
        except ValueError:
            print("EOF")

        # DVD MPEG-2
        print('\nDVD MPEG-2:')
        try:
            index = 0
            while True:
                index = s.index('\x00\x00\x01\xBA ', index)
                print('Start Offset: ' + hex(index))
                index = s.index('\x00\x00\x01\xB9', index + 4)
                print('End Offset: ' + hex(index))
                index += 4
        except ValueError:
            print("EOF")

        # MP4 MPEG-4
        print('\nMP4 MPEG-4:')
        try:
            index = 0
            while True:
                index = s.index('\x66\x74\x79\x70\x6D\x70\x34\x32', index)
                print('Start Offset: ' + hex(index - 4))
                index += 8
        except ValueError:
            print("EOF")
    return 0

#PDF
def PDFRecovery():
    print('\nPDF File Locations:')
    with open(filename, 'rb') as f:
        try:
            index = 0
            s = f.read()
            while True:
                index = s.index('\x25\x50\x44\x46', index)
                print('Start Offset: ' + hex(index))
                index += 4
        except ValueError:
            print("EOF")
    return 0

#BMP
def BMPRecovery():
    return 0

#GIF
def GIFRecovery():
    return 0

#JPG
def JPGRecovery():
    return 0

#DOCX
def DOCXRecovery():
    return 0

#AVI
def AVIRecovery():
    return 0

#PNG
def PNGRecovery():
    return 0

#Runner code

print('File size is: ' + str(hex(image_size)) + ' bytes')
MPGRecovery()
PDFRecovery()
BMPRecovery()
GIFRecovery()
JPGRecovery()
DOCXRecovery()
AVIRecovery()
PNGRecovery()
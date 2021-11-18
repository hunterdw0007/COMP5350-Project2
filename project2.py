# Hunter Westerlund and Charlotte Vance
# COMP 5350 Project 2

# References
# https://www.reddit.com/r/learnpython/comments/6m7ptm/find_hexadecimal_offset_of_certain_bytes_in/
# https://stackoverflow.com/questions/27001419/how-to-append-to-bytes-in-python-3
# https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
# https://www.geeksforgeeks.org/file-handling-python/
# https://id3.org/id3v2.3.0

# Recovery Steps
# 1. Scan disk image to find index of file header which is the start offset
# 2. Use the properties of the header to find the file size of that file
# 3. Use the file size to calculate the end offset
# 4. Collect the specified bytes and write those to a file

#imports
import sys
import os
import struct

# this is where the name of the disk image will come in
filename = sys.argv[1]
#filename = 'Project2.dd'

#finding the size of the disk image for later use
image_size = os.path.getsize(filename)

#Helper Code
# https://stuffivelearned.org/doku.php?id=misc:synchsafe
def unsynchsafe(num):
    out = 0
    mask = 0x7f000000
    for i in range(4):
        out >>= 1
        out |= num & mask
        mask >>= 8
    return out

#MPG
def MPGRecovery():
    print('\nMPG File locations:')
    with open(filename, 'rb') as f:
        total = 0

        s = f.read()

        # ID3 MP3
        print('\nID3 MP3:')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x49\x44\x33', index)
                print('Start Offset: ' + hex(index))
                synchsafefilesize = int.from_bytes(s[index + 6:index + 11], "big")
                filesizeint = unsynchsafe(synchsafefilesize)
                print('Filesize: ' + hex(filesizeint))
                print('End Offset: ' + hex(index + filesizeint))
                written_file = open("mp3-" + str(count) + ".mp3", "wb")
                written_file.write(s[index:index+filesizeint])
                written_file.close()
                print('File Written')
                print('')
                index += 3
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count

        # M4A
        print('\nM4A')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x66\x74\x79\x70\x4D\x34\x41\x20', index)
                print('Start Offset: ' + hex(index - 4))
                index += 8
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count

        # CD MPEG-1
        print('\nCD MPEG-1:')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x52\x49\x46\x46', index)
                if(index + 8 == s.index(b'\x43\x44\x58\x41', index)):
                    print('Start Offset: ' + hex(index))
                index += 4
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count

        # DVD MPEG-2
        print('\nDVD MPEG-2:')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x00\x00\x01\xBA ', index)
                print('Start Offset: ' + hex(index))
                index = s.index(b'\x00\x00\x01\xB9', index + 4)
                print('End Offset: ' + hex(index))
                index += 4
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count

        # MP4 MPEG-4
        print('\nMP4 MPEG-4:')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x66\x74\x79\x70\x6D\x70\x34\x32', index)
                print('Start Offset: ' + hex(index - 4))
                index += 8
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count
        print('\nTotal MPG types found: ' + str(total))
    return 0

#PDF
def PDFRecovery():
    print('\nPDF File Locations:')
    with open(filename, 'rb') as f:
        try:
            index = 0
            count = 0
            s = f.read()
            while True:
                index = s.index(b'\x25\x50\x44\x46', index)
                print('Start Offset: ' + hex(index))
                index += 4
                count += 1
        except ValueError:
            print("EOF")
        print('\nTotal PDF types found: ' + str(count))
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
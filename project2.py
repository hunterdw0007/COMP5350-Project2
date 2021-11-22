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

# MPG
# I cannot figure this one out
def MPGRecovery():
    print('\nMPG File locations:')
    with open(filename, 'rb') as f:
        total = 0

        s = f.read()

        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'', index)
                if(index % 512 != 0):
                    break
                print('Start Offset: ' + hex(index))
                index += 4
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count

        print('\nTotal MPG types found: ' + str(total))
    return 0

# PDF
def PDFRecovery():
    print('\nPDF File Locations:')

    # This will hold the start locations of the two PDFs so that we can search for the last footer
    start_locations = []

    with open(filename, 'rb') as f:
        try:
            index = 0
            count = 0
            s = f.read()

            # This loop finds the start index of the files
            while True:
                index = s.index(b'\x25\x50\x44\x46', index)
                start_locations.append(index)
                print('Start Offset: ' + hex(index))
                # Question: How to find the end of the PDF File if there are multiple footers in the file?
                # Writing the file to a new pdf file
                # written_file = open("pdf-" + str(count) + ".pdf", "wb")
                # written_file.write(s[index:index+filesizeint])
                # written_file.close()
                # print('File Written')
                print('')

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
    print('\nAVI File locations:')
    with open(filename, 'rb') as f:
        total = 0

        s = f.read()

        print('\nAVI:')
        try:
            index = 0
            count = 0
            while True:
                index = s.index(b'\x52\x49\x46\x46', index)
                if(index + 8 != s.index(b'\x41\x56\x49\x20\x4C\x49\x53\x54', index)):
                    break
                if(index % 512 != 0):
                    break
                print('Start Offset: ' + hex(index))
                avi_size = int.from_bytes(s[index + 4:index + 8], 'little', signed=False)
                print(hex(avi_size))
                written_file = open("avi-" + str(count) + ".avi", "wb")
                written_file.write(s[index:index + avi_size + 1])
                written_file.close()
                print('File Written')
                index += 4
                count += 1
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
        total += count
        print('\nTotal AVI types found: ' + str(count))

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
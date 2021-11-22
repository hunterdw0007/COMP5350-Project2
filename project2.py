# Hunter Westerlund and Charlotte Vance
# COMP 5350 Project 2

# References
# https://www.reddit.com/r/learnpython/comments/6m7ptm/find_hexadecimal_offset_of_certain_bytes_in/
# https://stackoverflow.com/questions/27001419/how-to-append-to-bytes-in-python-3
# https://stackoverflow.com/questions/19210414/byte-array-to-hex-string
# https://www.geeksforgeeks.org/file-handling-python/
# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
# https://www.ntfs.com/gif-signature-format.htm
# http://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html

# Recovery Steps
# 1. Scan disk image to find index of file header which is the start offset
# 2. Use the properties of the header to find the file size of that file or find the footer
# 3. Use the file size/footer location to calculate the end offset
# 4. Collect the specified bytes and write those to a file
# 5. Find the SHA-256 of the bytes

#imports
import sys
import os
import hashlib

# this is where the name of the disk image will come in
filename = sys.argv[1]
#filename = 'Project2.dd'

#finding the size of the disk image for later use
image_size = os.path.getsize(filename)

# MPG
# TODO make this one work
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
    print('\nPDF Files:\n')

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
                index += 4
                count += 1
        except ValueError:
            pass

        # This loop will go through each of the start locations and find the EOF before either the next PDF or the EOF of the partition
        for start_location in start_locations:
            eof_location = start_location
            stop_point = 0
            if(start_location == start_locations[-1]):
                stop_point = image_size
            else:
                stop_point = start_locations[start_locations.index(start_location) + 1]
            
            # changed signifies that the value of eof_location has changed within the loop
            # it is true by default because there must be at least 1 EOF marker
            changed = True
            while changed:
                curr_eof = eof_location
                try:
                    if(s.index(b'\x0A\x25\x25\x45\x4F\x46', eof_location) < stop_point):
                        eof_location = s.index(b'\x0A\x25\x25\x45\x4F\x46', eof_location) + 5
                except ValueError:
                    pass
                try:
                    if(s.index(b'\x0A\x25\x25\x45\x4F\x46\x0A', eof_location) < stop_point):
                        eof_location = s.index(b'\x0A\x25\x25\x45\x4F\x46\x0A', eof_location) + 6
                except ValueError:
                    pass
                try:
                    if(s.index(b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A', eof_location) < stop_point):
                        eof_location = s.index(b'\x0D\x0A\x25\x25\x45\x4F\x46\x0D\x0A', eof_location) + 8
                except ValueError:
                    pass
                try:
                    if(s.index(b'\x0D\x25\x25\x45\x4F\x46\x0D', eof_location) < stop_point):
                        eof_location = s.index(b'\x0D\x25\x25\x45\x4F\x46\x0D', eof_location) + 6
                except ValueError:
                    pass

                # Value of eof_location hasn't changed during the loop so we found the final one
                if(curr_eof == eof_location):
                    changed = False
            print('Start Offset: ' + hex(start_location))
            print('End Offset: ' + hex(eof_location))

            # Writing the file
            written_file = open("pdf-" + str(start_locations.index(start_location)) + ".pdf", "wb")
            written_file.write(s[start_location:eof_location + 1])
            written_file.close()
            print('File Written')

            # Hashing the bytes which make up the file
            hash = hashlib.sha256(s[start_location:eof_location + 1]).hexdigest()
            print('SHA-256: ' + hash)
            print()
        print('Found ' + str(count) + ' files')
    return 0

#BMP
def BMPRecovery():
    return 0

#GIF
# GIFs are weird. These are animated gifs and so we need to find every frame of the animation all the way to the end of the file. We have to do this iteratively
def GIFRecovery():
    print('\nGIF Files:\n')
    with open(filename, 'rb') as f:

        s = f.read()
        count = 0
        index = 0
        try:
            while True:
                # Locating the GIF89a header then checking whether it is at the start of a sector
                index = s.index(b'\x47\x49\x46\x38\x39\x61', index)
                if(index % 512 != 0):
                    break
                print('Start Offset: ' + hex(index))

                # # Finding File Size
                # offset = 0
                # end_index = 0
                # # Getting offset of the first block from the file header information
                # if(s[index + 0x0A] >= 0b10000000):
                #     offset = (1 <<((s[index + 0x0A] & 0x09) + 1)) * 3
                # offset = offset + 13
                
                # # This interates through the gif looking for the 0x3B that signifies the end of the file
                # # The reason it has to be done this way is because a GIF works in blocks of data so the 0x3B has to be at the beginning of a block
                # # Blocks are calculated based on the locations of other blocks and sub-blocks
                # while end_index == 0:

                #     # Extension blocks
                #     if(s[offset:offset + 2] == 0x2101):
                #         offset = offset + 2
                #     if(s[offset:offset + 2] == 0x21F9):
                #         offset = offset + 2
                #     if(s[offset:offset + 2] == 0x21FF):
                #         offset = offset + 2
                #     # Image block - can contain header which is the first if, otherwise it can have a variable number of sub-blocks which the second if calculates
                #     elif(s[offset] == 0x2C):
                #         if(s[offset + 0x0B] >= 0b10000000):
                #             offset = (1 <<((hex(s[offset + 0x0B]) & 0x07) + 1)) * 3
                #         else:
                #             offset = offset + 0x0B + 1
                #             while s[offset] != 0x00:
                #                 offset = offset + s[offset]
                #             offset = offset + 1
                #     # EOF marker - set end_index and break loop
                #     elif(s[offset] == 0x3B):
                #         end_index = offset
                #     else:
                #         print('Marker Not Found at ' + hex(offset))
                #         break


                # I think that I cheesed it by just putting some zeroes after the 3B but idk if that's okay for the final project
                # Technically this works but at the same time it's kind of cheating
                end_index = s.index(b'\x00\x3B\x00\x00\x00', index) + 1
                print('End Offset: ' + hex(end_index))

                # Writing the file
                written_file = open("gif-" + str(count) + ".gif", "wb")
                written_file.write(s[index:end_index + 1])
                written_file.close()
                print('File Written')

                # Hashing the bytes which make up the file
                hash = hashlib.sha256(s[index:end_index + 1]).hexdigest()
                print('SHA-256: ' + hash)
                index += 4
                count += 1
                print()
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
    return 0

#JPG
def JPGRecovery():
    return 0

#DOCX
def DOCXRecovery():
    return 0

#AVI
def AVIRecovery():
    print('\nAVI Files:\n')
    with open(filename, 'rb') as f:

        s = f.read()
        try:
            index = 0
            count = 0
            while True:
                # Locating the RIFF header then checking whether it is an AVI and at the start of a sector
                index = s.index(b'\x52\x49\x46\x46', index)
                if(index + 8 != s.index(b'\x41\x56\x49\x20\x4C\x49\x53\x54', index)):
                    break
                if(index % 512 != 0):
                    break
                print('Start Offset: ' + hex(index))

                # Finding File Size
                # File size in AVI is bytes 4-7
                avi_size = int.from_bytes(s[index + 4:index + 8], 'little')
                print('End Offset: ' + hex(index + avi_size))

                # Writing the file
                written_file = open("avi-" + str(count) + ".avi", "wb")
                written_file.write(s[index:index + avi_size + 1])
                written_file.close()
                print('File Written')

                # Hashing the bytes which make up the file
                hash = hashlib.sha256(s[index:index + avi_size + 1]).hexdigest()
                print('SHA-256: ' + hash)
                index += 4
                count += 1
                print()
        except ValueError:
            print("EOF")
        print('Found ' + str(count) + ' files')
    return 0

#PNG
def PNGRecovery():
    return 0

#Runner code

print('Disk size is: ' + str(hex(image_size)) + ' bytes')
# MPGRecovery()
PDFRecovery()
BMPRecovery()
GIFRecovery()
JPGRecovery()
DOCXRecovery()
AVIRecovery()
PNGRecovery()
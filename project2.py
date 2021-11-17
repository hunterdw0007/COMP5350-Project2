# Hunter Westerlund and Charlotte Vance
# COMP 5350 Project 2

# References
# https://www.reddit.com/r/learnpython/comments/6m7ptm/find_hexadecimal_offset_of_certain_bytes_in/
# https://stackoverflow.com/questions/27001419/how-to-append-to-bytes-in-python-3
# https://stackoverflow.com/questions/19210414/byte-array-to-hex-string

#imports
import sys
import os
import binascii

# this is where the name of the disk image will come in
filename = sys.argv[1]
#filename = 'Project2.dd'

#finding the size of the disk image for later use
image_size = os.path.getsize(filename)
print('File size is: ' + str(hex(image_size)) + ' bytes')

#MPG
print('\nMPG File locations:')
with open(filename, 'rb') as f:
    s = f.read()
    header = bytearray(b'\x00\x00\x01')
    for i in range(0xb0, 0xc0):
        try:
            header.append(i)
            print(binascii.hexlify(header).decode('ascii'))
            # TODO fix problem where it finds way too many things 
            index = 0
            while True:
                index = s.index(header, index)
                print('Start Offset: ' + hex(index))
                index += 4
        except ValueError:
            print("EOF")
            header.pop()


#PDF
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

#BMP
#GIF
#JPG
#DOCX
#AVI
#PNG
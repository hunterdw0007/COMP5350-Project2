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

#finding the size of the disk image for later use
image_size = os.path.getsize(filename)
print('File size is: ' + str(image_size) + ' bytes')

#MPG
print('\nMPG File locations:')
with open(filename, 'rb') as f:
    s = f.read()
    header = bytearray(b'\x00\x00\x01')
    for i in range(0xb0, 0xc0):
        try:
            header.append(i)
            print(binascii.hexlify(header).decode('ascii'))
            # TODO Implement way for searching past first index and always reach EOF
            print('Start Offset: ' + hex(s.index(header)))
            header.pop()
        except ValueError:
            print("EOF")
            header.pop()




#PDF
print('\nPDF File Locations:')
with open(filename, 'rb') as f:
    s = f.read()
    print('Start Offset: ' + hex(s.index(b'\x25\x50\x44\x46')))

#BMP
#GIF
#JPG
#DOCX
#AVI
#PNG
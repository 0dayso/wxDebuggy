#----------------------------------------------------------------------
# This file was generated by C:\Documents and Settings\Marty\My Documents\Python\wxVerilogViewer\hierarchy\encode_bitmaps.py
#
from wx import ImageFromStream, BitmapFromImage
from wx import EmptyIcon
import cStringIO


def getBlackData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\
\x00\x00\x00\x90\x91h6\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\xe1O\xe0\x00\x00\
\x00AIDAT(\x91c\xfc\xff\xff?\x03)\x80\x05\xcebdd\xc4\xa3\x0en.\x0bVQ4\x80l\
\x16\x0bA\xb3\x91\xf5\xfc\xff\xff\x9f\x05n0\x91Nb"h6\x1a\x18u\xd2\xe0p\x12JZ\
"\xca*R\x937\x00\xae\xf502\x8a`J9\x00\x00\x00\x00IEND\xaeB`\x82' 

def getBlackBitmap():
    return BitmapFromImage(getBlackImage())

def getBlackImage():
    stream = cStringIO.StringIO(getBlackData())
    return ImageFromStream(stream)

def getBlackIcon():
    icon = EmptyIcon()
    icon.CopyFromBitmap(getBlackBitmap())
    return icon

#----------------------------------------------------------------------
def getBlueData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\
\x00\x00\x00\x90\x91h6\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\xe1O\xe0\x00\x00\
\x00IIDAT(\x91c\xfc\xff\xff?\x03)\x80\x05\xcebdl\xc4\xa3\xee\xff\xffzt\r\x0c\
\x0c\x0c\x0c\r\xf5\xd8\x957 \xccb!h6\xb2\xfd\xff\xff\xd7\xb3\xc0\xad#\xd2IL\
\x04\xcdF\x03\xa3N\x1a\x1cNBKKDXEj\xf2\x06\x00\x01\xed00\xe0\xfd\xa8\xc8\x00\
\x00\x00\x00IEND\xaeB`\x82' 

def getBlueBitmap():
    return BitmapFromImage(getBlueImage())

def getBlueImage():
    stream = cStringIO.StringIO(getBlueData())
    return ImageFromStream(stream)

#----------------------------------------------------------------------
def getGreenData():
    return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\
\x00\x00\x00\x90\x91h6\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\xe1O\xe0\x00\x00\
\x00PIDAT(\x91\xed\x92;\x0e\xc0 \x0cC\x9d\xaa\xf7\x0e9\xf9\xebT\xda \xa0b\
\xeb\x80\x95!\x83\x7f\x83\r\xd0\n\xce\xfaY\xd8\x84\x87\xd3\n$\xc9\x07\xf4\
\xc8\ts\xefw>\x8e\xb8\xa1"1\xb8\xf2\xd0\x8eO\xef\x06\xbb\xd2?*\xe5-E\xd7=G\
\xad\xce\xfb\x02\xba5\x84D\xeaC\xb5\xa5\x00\x00\x00\x00IEND\xaeB`\x82' 

def getGreenBitmap():
    return BitmapFromImage(getGreenImage())

def getGreenImage():
    stream = cStringIO.StringIO(getGreenData())
    return ImageFromStream(stream)

#----------------------------------------------------------------------
def getRedData():
    return \
"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x02\
\x00\x00\x00\x90\x91h6\x00\x00\x00\x03sBIT\x08\x08\x08\xdb\xe1O\xe0\x00\x00\
\x00FIDAT(\x91c\xfc\xff\xff?\x03)\x80\x05\xc1dd\xc4\xa7\x10f.\x0b\xb2\xe0\
\xc1\x03\x07\xb0*\xb6wp@\xb5\x01\xbf\xd9\xc8\xf6\xff\xff\xcf\x82\xb0\x8e8'1\
\x116\x1b\x15\x8c:ip8\x89\x11\x91ZIN|\xc4\xa5s\x00\x9a\xa4'-\x04\xfc\x87a\
\x00\x00\x00\x00IEND\xaeB`\x82" 

def getRedBitmap():
    return BitmapFromImage(getRedImage())

def getRedImage():
    stream = cStringIO.StringIO(getRedData())
    return ImageFromStream(stream)


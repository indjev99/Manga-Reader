# text_voicer.py

from azure_speech_creator import execute_text_to_speech
from shapely.geometry import Point


def voice_text_on_image(id, relativeX, relativeY, image_blob_lists, image_sizes):
    x = image_sizes[id].width * relativeX
    y = image_sizes[id].height * relativeY
    pos = Point(x, y)
    print('..................   x: ' + str(x) + ' y: ' + str(y))

    txt = ""
    for blob in image_blob_lists[id]:
        if blob[1].contains(pos):
            txt = blob[0]
            break
    
    if txt != "":
        print('        found:       ' + txt)
        execute_text_to_speech(txt)
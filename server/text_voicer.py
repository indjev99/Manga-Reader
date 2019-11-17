# text_voicer.py

from azure_speech_creator import play_speech_file
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


lastPlayed = (-1, -1, -1)
def voice_text_on_image(id, relativeX, relativeY, image_blob_lists, image_sizes, url_hash):
    global lastPlayed

    x = image_sizes[id][0] * relativeX
    y = image_sizes[id][1] * relativeY
    pos = Point(x, y)

    valid = [i for i in range(len(image_blob_lists[id]))
             if Polygon(image_blob_lists[id][i][1]).contains(pos)]

    if len(valid) == 0 or len(valid) >= 2:
        lastPlayed = (-1, -1, -1)
    elif (url_hash, id, valid[0]) != lastPlayed:
        lastPlayed = (url_hash, id, valid[0])
        play_speech_file(url_hash, id, valid[0])
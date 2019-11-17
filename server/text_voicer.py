# text_voicer.py

from azure_speech_creator import play_speech_file
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


lastPlayed = ('', -1)
def voice_text_on_image(id, relativeX, relativeY, image_blob_lists, image_urls, image_sizes, output_language):
    global lastPlayed

    x = image_sizes[id].width * relativeX
    y = image_sizes[id].height * relativeY
    pos = Point(x, y)

    valid = [i for i in range(len(image_blob_lists[id]))
             if Polygon(image_blob_lists[id][i][1]).contains(pos)]

    if len(valid) == 0 or len(valid) >= 2:
        lastPlayed = (-1, -1, -1)
    else:
        blob_id = valid[0]
        image_url = image_urls[id]
        if (image_url, blob_id) != lastPlayed:
            lastPlayed = (image_url, blob_id)
            play_speech_file(image_url, blob_id, output_language)
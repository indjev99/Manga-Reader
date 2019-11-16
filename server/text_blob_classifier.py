# text_blob_classifier.py

import math
import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry.polygon import Polygon
from collections import namedtuple
import requests
import cv2

TextBoxParams = namedtuple('TextBoxParams', 'text_size text_angle center left_side_middle')


def check_same_blob(box1_params, box2_params):
    if not (box1_params.text_size <= box2_params.text_size * 1.5 and
            box1_params.text_size * 1.5 >= box2_params.text_size):
        return False

    ang_diff = min(abs(box1_params.text_angle - box2_params.text_angle),
                   abs(2 * math.pi - abs(box1_params.text_angle - box2_params.text_angle)))
    if not (ang_diff <= math.radians(10)):
        return False

    dist_side = np.linalg.norm(box1_params.left_side_middle - box2_params.left_side_middle)
    dist_cent = np.linalg.norm(box1_params.center - box2_params.center)
    avg_text_size = (box1_params.text_size + box2_params.text_size) // 2
    if not ((avg_text_size * 2 >= dist_side) or
            (avg_text_size * 2 >= dist_cent)):
        return False

    return True


def update_bbox(bbox, text_box):
    bbox.extend([np.array([text_box[1][0], text_box[1][1]]),
                np.array([text_box[1][2], text_box[1][3]]),
                np.array([text_box[1][4], text_box[1][5]]),
                np.array([text_box[1][6], text_box[1][7]])])
    return bbox


def group_into_blobs(text_boxes, box_params):
    child = {}
    for i in range(len(box_params)):
        for j in range(i + 1, len(box_params)):
            if check_same_blob(box_params[i], box_params[j]):
                child[i] = j
                break

    blobs = []
    used = {}
    for i in range(len(box_params)):
        if i not in used:
            txt = ''
            bbox = []
            j = i
            while j in child:
                text_box = text_boxes[j]
                txt = txt + text_box[0] + ' '
                bbox = update_bbox(bbox, text_box)
                used[j] = True
                j = child[j]

            used[j] = True
            text_box = text_boxes[j]
            txt = txt + text_box[0] + ' '
            bbox = update_bbox(bbox, text_box)

            bboxidx = ConvexHull(np.array(bbox)).vertices
            bbox = np.array([bbox[idx] for idx in bboxidx])
            blobs.append((txt, bbox))

    return blobs


def make_polygon(points):
    poly = Polygon(points)
    return poly


def analyze_image(text_boxes):
    box_params = []
    for text_box in text_boxes:
        pts = np.array(
            [[text_box[1][0], text_box[1][1]],
             [text_box[1][2], text_box[1][3]],
             [text_box[1][4], text_box[1][5]],
             [text_box[1][6], text_box[1][7]]], np.int32)

        mid1 = (pts[1] + pts[0]) // 2
        mid2 = (pts[2] + pts[3]) // 2
        side = (pts[0] + pts[3]) // 2
        seglen = np.linalg.norm(mid1 - mid2)
        angle = math.atan2(mid1[0] - mid2[0], mid1[1] - mid2[1])
        box_params.append(TextBoxParams(seglen, angle, (np.array(mid2) + np.array(mid1)) / 2, side))
    blobs = group_into_blobs(text_boxes, box_params)
    poly_blobs = [(txt, make_polygon(hull)) for (txt, hull) in blobs]
    return poly_blobs


# Drawing functions
def extract_image(image_url):
    r = requests.get(image_url, allow_redirects=True)
    img = cv2.imdecode(np.asarray(bytearray(r.content), dtype="uint8"), cv2.IMREAD_COLOR)
    return img


def image_add_boundary(img, p1, p2, pts, s):
    pts = pts.reshape((-1, 1, 2))
    img = cv2.line(img, p1, p2, (255, 255, 0), 5)
    cp = (np.array(p1) + np.array(p2)) // 2
    img = cv2.circle(img, tuple(cp), 3, (0, 255, 0), 3)
    img = cv2.circle(img, tuple(s), 3, (0, 0, 255), 3)
    return cv2.polylines(img, [pts], True, (0, 255, 255), 2)


def image_add_bbox(img, pts):
    return cv2.polylines(img, np.int32([pts]), True, (0, 255, 255), 2)

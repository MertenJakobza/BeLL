import cv2 as cv
import numpy as np
import math
import random as rn
from tqdm import tqdm


def verzeerung(opencv_list, bounding_list):
    bounding_list_ur = bounding_list
    img_list = []
    for a in tqdm(range(len(opencv_list)), desc="Verzerrung: "):
        # img = cv.imread(f"zwischen/bg_fertig{a}.png")
        img = opencv_list[a]
        rows, cols, ch = img.shape

        rands = []
        for c in range(8):
            rands.append(rn.randint(-int(rows / 200), int(rows / 200)))

        '''
        bounding1 = bounding_list_ur[a][1]
        pts1 = np.float32([[bounding1[1], bounding1[2]],
                           [bounding1[3], bounding1[2]],
                           [bounding1[1], bounding1[4]],
                           [bounding1[3], bounding1[4]]])
        pts2 = np.float32([[bounding1[1] + rands[0], bounding1[2] + rands[1]],
                           [bounding1[3] + rands[2], bounding1[2] + rands[3]],
                           [bounding1[1] + rands[4], bounding1[4] + rands[5]],
                           [bounding1[3] + rands[6], bounding1[4] + rands[7]]])'''

        coords = [int(rows / 2 - rows / 12), int(rows / 2 + rows / 12)]

        pts1 = np.float32(
            [[coords[0], coords[0]], [coords[1], coords[0]], [coords[0], coords[1]], [coords[1], coords[1]]])
        pts2 = np.float32([[coords[0] + rands[0], coords[0] + rands[1]], [coords[1] + rands[2], coords[0] + rands[3]],
                           [coords[0] + rands[4], coords[1] + rands[5]], [coords[1] + rands[6], coords[1] + rands[7]]])

        M = cv.getPerspectiveTransform(pts1, pts2)
        dst_img = cv.warpPerspective(img, M, (cols, rows))

        for b in range(len(bounding_list_ur[a]) - 1):
            xcoords = []
            ycoords = []
            x1y1 = np.array([[[bounding_list_ur[a][b + 1][1], bounding_list_ur[a][b + 1][2]]]], dtype="float32")
            newx1y1 = cv.perspectiveTransform(x1y1, M)  # transforrmieren
            # print(x1y1)
            xcoords.append(int(math.floor(newx1y1[0][0][0])))
            ycoords.append(int(math.floor(newx1y1[0][0][1])))

            x2y1 = np.array([[[bounding_list_ur[a][b + 1][3], bounding_list_ur[a][b + 1][2]]]], dtype="float32")
            newx2y1 = cv.perspectiveTransform(x2y1, M)  # transforrmieren
            # print(newx2y1)
            xcoords.append(int(math.floor(newx2y1[0][0][0])))
            ycoords.append(int(math.floor(newx2y1[0][0][1])))

            x1y2 = np.array([[[bounding_list_ur[a][b + 1][1], bounding_list_ur[a][b + 1][4]]]], dtype="float32")
            newx1y2 = cv.perspectiveTransform(x1y2, M)  # transforrmieren
            # print(newx1y2)
            xcoords.append(int(math.floor(newx1y2[0][0][0])))
            ycoords.append(int(math.floor(newx1y2[0][0][1])))

            x2y2 = np.array([[[bounding_list_ur[a][b + 1][3], bounding_list_ur[a][b + 1][4]]]], dtype="float32")
            newx2y2 = cv.perspectiveTransform(x2y2, M)  # transforrmieren
            # print(newx2y2)
            xcoords.append(int(math.floor(newx2y2[0][0][0])))
            ycoords.append(int(math.floor(newx2y2[0][0][1])))

            # print(xcoords, ycoords)
            # Ändern der Bounding Box Koordinaten
            bounding_list[a][b + 1][1] = min(xcoords)
            bounding_list[a][b + 1][2] = min(ycoords)
            bounding_list[a][b + 1][3] = max(xcoords)
            bounding_list[a][b + 1][4] = max(ycoords)

        bounding_list[a][0] = f"fertig{a}.png"

        # Bekomme Punkt, nach Verzerrung

        img_list.append(dst_img)
        # cv.imwrite(f"zwischen/pers{a}.png", dst_img)
        # print(f"Bild Nr. {a + 1} verzerrt.")
    return bounding_list, img_list


if __name__ == '__main__':
    verzeerung(0, [])

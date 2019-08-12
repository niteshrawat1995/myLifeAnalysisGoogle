import cv2
import os


WORD_IMAGES_DIR = os.path.join(os.getcwd(), "word_images_per_day")


# Linux:
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

out = cv2.VideoWriter('{}.avi'.format(os.path.join(
    WORD_IMAGES_DIR, "video.avi")), fourcc, 60.0, (1200, 700))

for i in range(2038):
    img_path = os.path.join(os.path.join(WORD_IMAGES_DIR, f"{i}.png"))
    print(img_path)
    frame = cv2.imread(img_path)
    out.write(frame)

out.release()

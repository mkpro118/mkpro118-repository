import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("Error opening video stream or file")

frame_width = int(camera.get(3))
frame_height = int(camera.get(4))

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('my_face.mp4', fourcc, 25, (frame_width, frame_height))

while camera.isOpened():
    ret, frame = camera.read()
    if ret:
        writer.write(frame)

        cv2.imshow('Frame', frame)

        # Press X to close the video
        if cv2.waitKey(25) & 0xFF == ord('x'):
            break
    else:
        break

camera.release()
writer.release()

cv2.destroyAllWindows()

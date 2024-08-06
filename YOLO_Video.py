from ultralytics import YOLO
import cv2
import math
import os

model = YOLO("YOLO-Weights/best_file.pt")
classNames = ['Ariel','Coca Cola','Colgate','Fanta','Kurkure','Lays Masala','Lays Mexican','Lifebuoy Soap','Sunsilk Shampoo','Vaseline Lotion']
def video_detection(path_x):
    video_capture = path_x
    #Create a Webcam Object
    cap=cv2.VideoCapture(video_capture)
    frame_width=int(cap.get(3))
    frame_height=int(cap.get(4))
    #out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P','G'), 10, (frame_width, frame_height))

    while True:
        success, img = cap.read()
        results=model(img,stream=True)
        for r in results:
            boxes=r.boxes
            for box in boxes:
                x1,y1,x2,y2=box.xyxy[0]
                x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                print(x1,y1,x2,y2)
                conf=math.ceil((box.conf[0]*100))/100
                cls=int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                print(t_size)
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                if class_name == 'Ariel':
                    color=(0, 204, 255)
                elif class_name == "Coca Cola":
                    color = (222, 82, 175)
                elif class_name == "Colgate":
                    color = (0, 149, 255)
                elif class_name == "Fanta":
                    color = (205, 92, 92)
                elif class_name == "Kurkure":
                    color = (199, 21, 133)
                elif class_name == "Lays Masala":
                    color = (255, 69, 0)
                elif class_name == "Lays Mexican":
                    color = (255, 255, 0)
                elif class_name == "Lifebuoy Soap":
                    color = (255, 0, 255)
                elif class_name == "Sunsilk Shampoo":
                    color = (0, 255, 0)
                elif class_name == "Vaseline Lotion":
                    color = (0, 255, 255)
                if conf>0.5:
                    cv2.rectangle(img, (x1,y1), (x2,y2), color,3)
                    cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)

        yield img
        #out.write(img)
        #cv2.imshow("image", img)
        #if cv2.waitKey(1) & 0xFF==ord('1'):
            #break
    #out.release()
cv2.destroyAllWindows()
# def object_count(video_path):
#     counter = {'Ariel': 0, 'Surf-Excel': 0, 'Tide': 0}
#
#     # Create a video generator
#     video_generator = video_detection(video_path)
#
#     for frame in video_generator:
#         results = model(frame)
#         for r in results:
#             for box in r.boxes:
#                 cls = int(box.cls[0])
#                 class_name = classNames[cls]
#                 if class_name in counter:
#                     counter[class_name] += 1
#
#     return counter
import os

def object_count(file_path):
    counter = {'Ariel':0,'Coca Cola':0,'Colgate':0,'Fanta':0,'Kurkure':0,'Lays Masala':0,'Lays Mexican':0,'Lifebuoy Soap':0,'Sunsilk Shampoo':0,'Vaseline Lotion':0}

    # Check the file extension to determine if it's an image or video
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp']:
        # Perform object detection on the image
        results = model(file_path)
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                class_name = classNames[cls]
                confidence = box.conf[0]
                if class_name in counter and confidence > 0.5:
                    counter[class_name] += 1
    elif file_extension.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.mpg', '.mpeg', '.webm', '.m4v']:
        # Create a video generator
        video_generator = video_detection(file_path)

        # Iterate over frames and count objects in each frame
        for frame in video_generator:
            results = model(frame)
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    class_name = classNames[cls]
                    confidence = box.conf[0]
                    if class_name in counter and confidence > 0.5:
                        counter[class_name] += 1

    return counter


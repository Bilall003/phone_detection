import cv2

cap = cv2.VideoCapture('sample.mp4')
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Getting frame from webcam
thres = 0.6 # Threshold to detect object

def detect_faces(img):
    return False


while True:
    _, image = cap.read()

    classIds, confs, bbox = net.detect(image,confThreshold=thres)

    list_of_people = []

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            if classId == 1:
                

                top = box[0]
                left = box[1]

                bottom = top+box[2]
                right = left+box[3]

                img = image[left:right,top:bottom]

                found = detect_faces(img)

                if found:
                    cv2.rectangle(image,box,color=(0,255,0),thickness=2)
                else:
                    cv2.rectangle(image,box,color=(0,0,255),thickness=2)



                cv2.imshow('cropped',img)
                cv2.waitKey()
                # list_of_people.append(img)
    


    # cv2.imshow('Live camera',image)
    # cv2.waitKey(1)
import os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from ui_main_window import *
import sys


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.display_cam = False
        self.start = False


        # Run the camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.showcam)
        self.controlTimer()


        self.cap.set(3,1280)
        self.cap.set(4,720)
        self.cap.set(10,70)

        self.classNames= []
        classFile = 'coco.names'
        with open(classFile,'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = 'frozen_inference_graph.pb'

        self.net = cv2.dnn_DetectionModel(weightsPath,configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)



        self.ui.show_btn.clicked.connect(lambda:self.display_camera_clicked())
        self.ui.start_btn.clicked.connect(lambda:self.start_clicked())


        with open('theme.qss', 'r') as f:
            stylee = f.read()
            self.setStyleSheet(stylee)

        
    def controlTimer(self):
        """
        This method takes camera input for display
        # """

        self.cap = cv2.VideoCapture(0)

        self.timer.start(20)

    def showcam(self):  
        
        """
        This method displays frame of given camera

        Camera input is taken by a timer
        """
        
        
        # Getting frame from webcam
        _, self.image = self.cap.read()

        if self.start:

            thres = 0.6 # Threshold to detect object
            classIds, confs, bbox = self.net.detect(self.image,confThreshold=thres)
            print(classIds,bbox)

            if len(classIds) != 0:
                for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                    if classId == 77:
                        self.start = False
                        cv2.rectangle(self.image,box,color=(0,255,0),thickness=2)
                        cv2.putText(self.image,self.classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                        cv2.putText(self.image,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

                        path = os.getcwd()
                        path = os.path.join(path,'detected_images')
                        
                        name = 0
                        for p in os.listdir(path):
                            name+=1
                        
                        name = str(name)+'.jpg'

                        path = os.path.join(path,name)

                        cv2.imwrite(path,self.image)
                        
                        os.system('x.png')

        
        if self.display_cam:
            cv2.imshow('Live camera',self.image)
        else:
            cv2.destroyAllWindows()
    
    def display_camera_clicked(self):
        if self.ui.show_btn.text() == 'Show cam':
            self.ui.show_btn.setText('Hide cam')
            self.display_cam = True

        else:
            self.ui.show_btn.setText('Show cam')
            self.display_cam = False

    def start_clicked(self):
        if self.ui.start_btn.text() == 'Start':
            self.ui.start_btn.setText('Stop')
            self.start = True

        else:
            self.ui.start_btn.setText('Start')
            self.start = False

        



if __name__ == '__main__':

    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
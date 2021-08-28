# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 14:59:10 2021

@author: elif_seker
"""
from cv2 import destroyAllWindows, VideoCapture, resize, waitKey, rectangle, putText, dnn, FONT_HERSHEY_SIMPLEX, imshow, flip
from numpy import argmax, array

cap = VideoCapture(0)

a = 318

while True:
    print("-->")
    redline = 0
    ret, frame = cap.read()

    r = rectangle(frame, (0, 4160), (410, a), (0, 0, 255), thickness=2)

    frame = flip(frame, 1)
    frame = resize(frame, (416, 416))

    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    frame_blob = dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

    labels = ["class değerleri(tek tek)"]

    model = dnn.readNetFromDarknet("cfg_dosyası",
                                   "weights_dosyası")

    layers = model.getLayerNames()
    output_layer = [layers[layer[0] - 1] for layer in model.getUnconnectedOutLayers()]

    model.setInput(frame_blob)

    detection_layers = model.forward(output_layer)

    ############## NON-MAXIMUM SUPPRESSION - OPERATION 1 ###################

    ids_list = []
    boxes_list = []
    confidences_list = []

    ############################ END OF OPERATION 1 ########################

    for detection_layer in detection_layers:
        for object_detection in detection_layer:

            scores = object_detection[5:]
            predicted_id = argmax(scores)
            confidence = scores[predicted_id]

            if confidence > 0.20:
                label = labels[predicted_id]
                bounding_box = object_detection[0:4] * array([frame_width, frame_height, frame_width, frame_height])
                (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")

                start_x = int(box_center_x - (box_width / 2))
                start_y = int(box_center_y - (box_height / 2))

                ############## NON-MAXIMUM SUPPRESSION - OPERATION 2 ###################

                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([start_x, start_y, int(box_width), int(box_height)])

                ############################ END OF OPERATION 2 ########################

    ############## NON-MAXIMUM SUPPRESSION - OPERATION 3 ###################

    max_ids = dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)

    for max_id in max_ids:

        max_class_id = max_id[0]
        box = boxes_list[max_class_id]

        start_x = box[0]
        start_y = box[1]
        box_width = box[2]
        box_height = box[3]

        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]

        ############################ END OF OPERATION 3 ########################

        end_x = start_x + box_width
        end_y = start_y + box_height
        
        
        label = "{}: {:.2f}%".format(label, confidence * 100)
        print("predicted object {}".format(label))


        # kendi sistemimizde kırmızı alan tehlikeli bölge olarak ayarladığımız için bu ayarı koydum. 
        if end_y >= a:
            print("kırmızı alan uyarısı!".format(label))

    imshow("Detector", frame)

# %%
cap.release()
destroyAllWindows()

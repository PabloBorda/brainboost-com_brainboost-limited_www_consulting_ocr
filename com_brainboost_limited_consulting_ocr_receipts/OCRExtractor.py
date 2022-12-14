from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import cv2
import math


pytesseract.pytesseract.tesseract_cmd = r'tesseract'


class OCRExtractor:
    
    
    @classmethod
    def image_to_text(cls,path_to_image):
        coordinates_and_detected_text = []
        

        
        
        # grab the number of rows and columns from the scores volume, then
        # initialize our set of bounding box rectangles and corresponding
        # confidence scores
        def decode_predictions(scores, geometry):
            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []
            
            
            # extract the scores (probabilities), followed by the
            # geometrical data used to derive potential bounding box
            # coordinates that surround text
            for y in range(0, numRows):
                scoresData = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]
                
                # loop over the number of columns
                for x in range(0, numCols):
                    #0.5 is min confidence, confidence range is 0 ~ 1.
                    if scoresData[x] < 0.5:
                        continue
                    # compute the offset factor as our resulting feature
                    # maps will be 4x smaller than the input image
                    (offsetX, offsetY) = (x * 4.0, y * 4.0)
                    
                    # extract the rotation angle for the prediction and
                    # then compute the sin and cosine
                    
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)
                    
                    # use the geometry volume to derive the width and height
                    # of the bounding box
                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]
                    
                    # compute both the starting and ending (x, y)-coordinates
                    # for the text prediction bounding box
                    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                    startX = int(endX - w)
                    startY = int(endY - h)
                    
                    rects.append((startX, startY, endX, endY))
                    confidences.append(scoresData[x])
                    
            return (rects, confidences)
        
        image = cv2.imread(path_to_image)
        orig = image.copy()
        (origH, origW) = image.shape[:2]
        #print(origH, origW)
        
        # set the new width and height and then determine the ratio in change
        # for both the width and height
        #(newW, newH) = (args["width"], args["height"])

        (newW, newH) = (math.ceil(origW/32)*32, math.ceil(origH/32)*32) 
        rW = origW / float(newW)
        rH = origH / float(newH)
        
        image = cv2.resize(image, (newW, newH))
        (H, W) = image.shape[:2]
        
        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text

        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]
        
        net = cv2.dnn.readNet('com_brainboost_limited_consulting_ocr_receipts/frozen_east_text_detection.pb')
        
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), swapRB=True, crop=False)
        
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        
        (rects, confidences) = decode_predictions(scores, geometry)
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        #print(boxes)
        
        # initialize the list of results

        results = []
        
        for (startX, startY, endX, endY) in boxes:
            
            # scale the bounding box coordinates based on the respective
            # ratios
            
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)
            
            dX = 2
            dY = 4
            
            # apply padding to each side of the bounding box, respectively

            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(origW, endX + (dX * 2))
            endY = min(origH, endY + (dY * 2))
            
            
            # extract the actual padded ROI

            roi = orig[startY:endY, startX:endX]
            
            text = pytesseract.image_to_string(roi,config='-l eng --oem 1 --psm 7')
        
            # add the bounding box coordinates and OCR'd text to the list
            # of results

            results.append(((startX, startY, endX, endY), text))
            
        
        # sort the results bounding box coordinates from top to bottom
        
        results = sorted(results, key=lambda r:r[0][1])
        #output = orig.copy()
        #print("[startX,startY,endX,endY]=[Text]\n")
        
        
        for ((startX, startY, endX, endY), text) in results:
            
            text_normalized = text.replace('\n',' ')
            coordinates_and_detected_text.append((startX, startY, endX, endY, text_normalized))
            
        return coordinates_and_detected_text


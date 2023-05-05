from PIL import ImageGrab, ImageChops
import numpy as np
import tensorflow.keras as keras
from keras.models import load_model
from PIL import Image, ImageOps
from skimage.filters import threshold_otsu
import cv2
import json

# Save the y_label values to a file


class AlphabetRecognition:
    def __init__(self):
        self.model = load_model('emnistCNN.h5')
        self.pre_processed_images = []
        with open('y_label.txt', 'r') as f:
            self.y_label = json.load(f)
        # model = load_model('kar_model_balanced.h5')
        

    
    def get_bounding_boxes(self,image):
        # Get the connected components in the image
        components = ImageOps.autocontrast(image.convert('RGB'))

        # Get the bounding boxes of the connected components
        bounding_boxes = []
        for component in components.split():
            bounding_boxes.append(component.getbbox())

        return bounding_boxes


    def pre_process(self, img):
        img.save('input_image.png')
        threshold = 220
        binary_reversed = img.point(lambda x: 255 if x < threshold else 0)
        binary_reversed_array = np.array(binary_reversed)
        # Perform connected component analysis
        #label_image = binary_reversed.convert('L').point(lambda x: 255 - x)
        
        # Threshold using Otsu's method
        thresh = 0
        margin = 20
        try:
            thresh = threshold_otsu(binary_reversed_array)
            print(thresh)
        except ValueError:
            print("Image is empty")
        else:
            # Separate foreground and background using threshold
            mask = binary_reversed_array > thresh

            # Find bounding box of non-empty region
            coords = np.argwhere(mask)
            x0, y0 = coords.min(axis=0)
            x1, y1 = coords.max(axis=0) + 1
            print(x0,x1,y0,y1)
            # Crop image to non-empty region
            cropped_img = binary_reversed.crop((y0-margin, x0-margin, y1+margin, x1+margin))
            cropped_img = cropped_img.resize((28, 28))
            self.pre_processed_images.append(np.array(cropped_img))


    def pre_process_segmentation(self, img):
        img.save('input_image.png')
        threshold = 220
        binary_reverse = img.point(lambda x: 255 if x < threshold else 0)

        # Perform connected component analysis
        # label_image = binary.convert('L').point(lambda x: 255 - x)
        binary_reverse_array = np.array(binary_reverse)
        contours, _ = cv2.findContours(binary_reverse_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours from left to right and top to bottom
        bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
        bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[0], b[1]))

        # Merge bounding boxes that overlap in the x-axis
        margin = 10
        # Set the height limit check for finding and merging the dot for i and j
        height_limit = 50
        merged_boxes = []
        prev_box = bounding_boxes[0]
        for box in bounding_boxes[1:]:
            height_difference = 0
            if box[3] > prev_box[3]:
                height_difference = box[3] / prev_box[3]
            else:
                height_difference = prev_box[3] / box[3]
            if (box[0] > prev_box[0] - margin and box[0] < prev_box[0] + prev_box[2] + margin) \
                and (abs(prev_box[1]- box[1]) < height_limit) \
                    and (height_difference > 3):
                prev_box = (prev_box[0], min(prev_box[1], box[1]), max(box[0]+box[2], prev_box[0]+prev_box[2])-prev_box[0], max(box[1]+box[3], prev_box[1]+prev_box[3])-prev_box[1])
            else:
                merged_boxes.append(prev_box)
                prev_box = box
        merged_boxes.append(prev_box)

        padding = 10
        # Iterate over each merged bounding box and crop the corresponding shape from the original image
        for i, bbox in enumerate(merged_boxes):
            x, y, w, h = bbox
            region = binary_reverse.crop((x - padding, y - padding, x + w + padding, y + h + padding))
            region.save(f'region_{i}.png')
            region = region.resize((28, 28))
            self.pre_processed_images.append(np.array(region))
  
    
    def perdict(self):
        result = ''
        accuracy_treshhold = 0.80
        for inverted_data in self.pre_processed_images:
            # Reshape image data to make it ready for the model
            inverted_data = inverted_data.reshape(-1, 28, 28, 1)
            inverted_data = inverted_data.astype('float32') / 255

            # predict the labels of the test data
            y_pred = self.model.predict(inverted_data)
            # Check if accuracy is good enough and if not show the accuracy
            accuracy = y_pred[0,int(np.argmax(y_pred, axis=1))] 
            if accuracy >= accuracy_treshhold:
                result += self.y_label[str(int(np.argmax(y_pred, axis=1)))] + ' '
            else:
                result += self.y_label[str(int(np.argmax(y_pred, axis=1)))] + " (Acc=" + str(format(accuracy, '.2f')) + ") " 
            print(int(np.argmax(y_pred, axis=1)), accuracy)
        return result
    
    def process_image_single_letter(self,img):
        try:
            self.pre_process(img)
            result = self.perdict()
        except Exception:
            result = "No result, try again"
        
        return result
    
    def process_image_multiple_letters(self,img):
        try:
            self.pre_process_segmentation(img)
            result = self.perdict()
        except Exception:
            result = "No result, try again"
        return result



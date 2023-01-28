import cv2
import numpy as np

# load image
# img = cv2.imread('2.jpg')

image_path = 'input_images/earphone.jpg'
output_directory = "output_images/" 
extension = ".png"

img = cv2.imread(image_path)

# convert to graky
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# threshold input image as mask
mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

# negate mask
mask = 255 - mask

# apply morphology to remove isolated extraneous noise
# use borderconstant of black since foreground touches the edges
kernel = np.ones((3,3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# anti-alias the mask -- blur then stretch
# blur alpha channel
mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

# linear stretch so that 127.5 goes to 0, but 255 stays 255
mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

# put mask into alpha channel
result = img.copy()
result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
result[:, :, 3] = mask


final_path= output_directory + (image_path.rsplit(".", 1)[0]).split("/", 1)[1] + extension

cv2.imwrite(final_path , result)


# ALTERNATIVE WAY THAT NEED SOME WORK
# from rembg import remove 
# from PIL import Image

# input_path = 'input_images/earphone.jpg'
# output_path = 'output.png'
# input = Image.open(input_path)
# output = remove(input)
# output.save(output_path)

 




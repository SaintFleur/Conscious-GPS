import cv2
#import open cv
import numpy as np
#import numpy for scientific calculations
# from matplotlib import pyplot as plt
#display the image
# import imutils
# import glob
# import math



green=(0,255,0)
red=(255,0,0)
blue=(0,0,255)


def find_biggest_contour(image):
	# image = imutils.resize(image, width = 555 , height = 515)
	image=image.copy()

	# _ , contours , hierarchy=cv2.findContours(image,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	contours , hierarchy=cv2.findContours(image,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	contour_sizes=[(cv2.contourArea(contour),contour) for contour in contours]
	# if(len(contour_sizes) == 0 or contour_sizes == None):
	# 	print("None Found")
	# 	return None
	# else:
	if(contour_sizes == 0):
		return None, None
	else:
		biggest_contour=max(contour_sizes,key=lambda x:x[0])[1]
		mask=np.zeros(image.shape,np.uint8)

		cv2.drawContours(mask,[biggest_contour],-1,255,-1)

		# print("Maximum X Value of Biggest Contour: ", np.amax(biggest_contour[0]))
		# print("Minimum X Value of Biggest Contour: ", np.amin(biggest_contour[0]))
		# print("Mid X Point: ", (np.amax(biggest_contour[0]) + np.amin(biggest_contour[0])) / 2)

		# print("Maximum Y Value of Biggest Contour: ", np.amax(biggest_contour[1]))
		# print("Minimum Y Value of Biggest Contour: ", np.amin(biggest_contour[1]))
		# print("Mid Y Point: ", (np.amax(biggest_contour[1]) + np.amin(biggest_contour[1])) / 2)

		# cx, cy, area, perimeter = calculate_moments(biggest_contour)

		# print("cx: %s", str(cx))
		# print("cy: %s", str(cy))
		# print("area: %s", str(area))
		# print("perimeter: %s", str(perimter))
		return biggest_contour,mask

def overlay_mask(mask,image):
	rgb_mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
	img=cv2.addWeighted(rgb_mask,0.5,image,0.5,0)
	return img

def circle_contour(image,contour):

	image_with_ellipse=image.copy()

	h, w, channels = image_with_ellipse.shape
	# print("this is me")
	# print(w)
	# print (h)
	w = w/2
	h = h/2
	# print(w)
	# print (h)

	cv2.circle(image_with_ellipse, (w, h), 7, (255, 255, 255), -1)
	cv2.putText(image_with_ellipse, "image center", (w - 20, h - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	ellipse=cv2.fitEllipse(contour)

	cv2.ellipse(image_with_ellipse,ellipse,green,2,1)

	cX = (np.amax(contour[0]) + np.amin(contour[0])) / 2
	cY = (np.amax(contour[1]) + np.amin(contour[1])) / 2

	cv2.circle(image_with_ellipse, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(image_with_ellipse, "bus center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	return image_with_ellipse

def show(image):

	plt.figure(figsize=(10,10))
	plt.imshow(image,interpolation='nearest')

def draw_bus_stop(image):

	#PRE PROCESSING OF IMAGE

	# image = imutils.resize(image, width = 555 , height = 515)

	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

	maxsize=max(image.shape)

	scale=700/maxsize

	# image=cv2.resize(image,None,fx=scale,fy=scale)

	image_blur=cv2.GaussianBlur(image,(7,7),0)

	image_blur_hsv=cv2.cvtColor(image_blur,cv2.COLOR_RGB2HSV)

	#Green Range
	min_color=np.array([50,80,80])
	max_color=np.array([100,120,120])

	mask1=cv2.inRange(image_blur_hsv,min_color,max_color)

	#Red Range
	min_color2=np.array([160,200,190])
	max_color2=np.array([190,256,230])

	mask2=cv2.inRange(image_blur_hsv,min_color2,max_color2)

	#Blue Range
	min_color3=np.array([100,200,160])
	max_color3=np.array([135,256,200])

	mask3=cv2.inRange(image_blur_hsv,min_color3,max_color3)

	#Purple Range
	min_color4=np.array([135,140,100])
	max_color4=np.array([160,180,150])

	mask4=cv2.inRange(image_blur_hsv,min_color4,max_color4)

	# #White Range
	min_color5=np.array([80,0,190])
	max_color5=np.array([120,35,220])

	mask5=cv2.inRange(image_blur_hsv,min_color5,max_color5)

	mask=mask2+mask3+mask1+mask4-mask5

	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))

	mask_closed=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	mask_cleaned=cv2.morphologyEx(mask_closed,cv2.MORPH_OPEN,kernel)

	big_contour,mask_fruit=find_biggest_contour(mask_cleaned)

	if(big_contour == None and mask_fruit == None)
			return None, None
	else:
		overlay=overlay_mask(mask_cleaned,image)

		circled=circle_contour(overlay,big_contour)

		#show(circled)

		bgr=cv2.cvtColor(circled,cv2.COLOR_RGB2BGR)

		return bgr, big_contour


def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

# def draw_banana(image):

# 	#PRE PROCESSING OF IMAGE

# 	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

# 	maxsize=max(image.shape)

# 	scale=700/maxsize

# 	image=cv2.resize(image,None,fx=scale,fy=scale)

# 	image_blur=cv2.GaussianBlur(image,(7,7),0)

# 	image_blur_hsv=cv2.cvtColor(image_blur,cv2.COLOR_RGB2HSV)

# 	min_color=np.array([20,50,50])
# 	max_color=np.array([30,256,256])

# 	mask1=cv2.inRange(image_blur_hsv,min_color,max_color)

# 	min_color2=np.array([60,50,50])
# 	max_color2=np.array([70,256,256])

# 	mask2=cv2.inRange(image_blur_hsv,min_color2,max_color2)

# 	mask=mask1+mask2

# 	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))

# 	mask_closed=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
# 	mask_cleaned=cv2.morphologyEx(mask_closed,cv2.MORPH_OPEN,kernel)

# 	big_contour,mask_fruit=find_biggest_contour(mask_cleaned)

# 	overlay=overlay_mask(mask_cleaned,image)

# 	circled=circle_contour(overlay,big_contour)

# 	show(circled)

# 	bgr=cv2.cvtColor(circled,cv2.COLOR_RGB2BGR)

# 	return bgr


# def draw_strawberry(image):

# 	#PRE PROCESSING OF IMAGE

# 	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

# 	maxsize=max(image.shape)

# 	scale=700/maxsize

# 	image=cv2.resize(image,None,fx=scale,fy=scale)

# 	image_blur=cv2.GaussianBlur(image,(7,7),0)

# 	image_blur_hsv=cv2.cvtColor(image_blur,cv2.COLOR_RGB2HSV)

# 	min_color=np.array([0,100,80])
# 	max_color=np.array([10,256,256])

# 	mask1=cv2.inRange(image_blur_hsv,min_color,max_color)

# 	min_color2=np.array([170,100,80])
# 	max_color2=np.array([180,256,256])

# 	mask2=cv2.inRange(image_blur_hsv,min_color2,max_color2)

# 	mask=mask1+mask2

# 	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))

# 	mask_closed=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
# 	mask_cleaned=cv2.morphologyEx(mask_closed,cv2.MORPH_OPEN,kernel)

# 	big_contour,mask_fruit=find_biggest_contour(mask_cleaned)

# 	overlay=overlay_mask(mask_cleaned,image)

# 	circled=circle_contour(overlay,big_contour)

# 	show(circled)

# 	bgr=cv2.cvtColor(circled,cv2.COLOR_RGB2BGR)

# 	return bgr

# def calculate_moments(contour):
# 	cnt = contour[0]
# 	M = cv2.moments(cnt)
# 	print( M )
# 	cx = int(M['m10']/M['m00'])
# 	cy = int(M['m01']/M['m00'])

# 	area = cv2.contourArea(cnt)

# 	perimeter = cv2.arcLength(cnt,True)

# 	return cx, cy, area, perimeter



# #input image
# bus_stop=cv2.imread('bus.jpg')
# # banana=cv2.imread('banana.jpg')
# # strawberry=cv2.imread('berry.jpg')
# full_bus_stop=cv2.imread('bus_green.jpg')
# #process image
# result_bus_stop=draw_bus_stop(bus_stop)
# # result_banana=draw_banana(banana)
# # result_strawberry=draw_strawberry(strawberry)
# result_full_bus_stop=draw_bus_stop(full_bus_stop)


# #output image

# cv2.imwrite('bus_new.jpg',result_bus_stop)
# # cv2.imwrite('banana_new.jpg',result_banana)
# # cv2.imwrite('strawberry_new.jpg',result_strawberry)
# cv2.imwrite('bus_green_new.jpg',result_full_bus_stop)

count = 0
# images = [cv2.imread('photo_1.jpg'), cv2.imread('photo_2.jpg'), cv2.imread('photo_3.jpg'), cv2.imread('photo_4.jpg')
#                     , cv2.imread('false.jpg'), cv2.imread('bus.jpg')]


# def isBusStop(image, contour):


# for image in glob.glob("bus_images/*.jpg") or glob.glob("bus_images/*.png"):
# 	bus_stop= cv2.imread(image)

# 	# if(draw_bus_stop(bus_stop) == None):
# 	# 	break

# 	result_bus_stop, _=draw_bus_stop(bus_stop)
# 	#output image

# 	cv2.imwrite('result_' + str(count) + '.jpg',result_bus_stop)
# 	count+=1

# for image in glob.glob("angled/*.jpg"):
# 	bus_stop= cv2.imread(image)

# 	# if(draw_bus_stop(bus_stop) == None):
# 	# 	break
# 	result_bus_stop, _=draw_bus_stop(bus_stop)
# 	#output image

# 	cv2.imwrite('result_' + str(count) + '.jpg',result_bus_stop)
# 	count+=1


def calculateXDistance(image):

	result_image, contour = draw_bus_stop(image)

	if(result_image	== None and contour == None):
		print("No contour found, distance cannot be calcualed")
		return None, None

	# contour, _ = find_biggest_contour(result_image)

	else:

		image_height, image_width, channels = image.shape

		center_X = image_width/2
		center_Y = image_height/2

		cX = (np.amax(contour[0]) + np.amin(contour[0])) / 2
		cY = (np.amax(contour[1]) + np.amin(contour[1])) / 2

		print(str("Image Center: (", center_X, ", ", center_Y, ")"))
		print(str("Bus Center: (", cX, ", ", cY, ")"))
		distance = center_X	 - cX

		return distance, image_width


# calculateXDistance(cv2.imread("bus.jpg"))

# import urllib.request
import cv2
import numpy as np
import os
import glob

def store_raw_images():
	neg_images_link = ''
	neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()

	if not os.path.exists('neg'):
		os.makedirs('neg')

		pic_num = 1

		for i in neg_image_urls.split('\n'):
			try:
				print(i)
				urllib.request.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
				img = cv2.imread("neg/"+str(pic_num)+'.jpg', cv2.IMREAD_GRAYSCALE)
				resized_image = cv2.resize(img, (100, 100))
				cv2.imwrite("neg/"+str(pic_num)+'.jpg', resized_image)

			except Exception as e:
				print(str(e))


def store_raw_images_from_dir(): 
	neg_images_path = ''
	# neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()

	pic_num = 1

	for image in glob.glob("All/*.jpg"):#or glob.glob("All/*.png") or glob.glob("All/*.jpeg"):
	

		if not os.path.exists('neg'):
			os.makedirs('neg')

		try:
			# print(i)
			# urllib.request.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
			img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
			resized_image = cv2.resize(img, (100, 100))
			cv2.imwrite("neg/"+str(pic_num)+".jpg", resized_image)
			pic_num+=1

		except Exception as e:
			print(str(e))
	for image in glob.glob("All/*.jpeg"):
	

		if not os.path.exists('neg'):
			os.makedirs('neg')

		try:
			# print(i)
			# urllib.request.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
			img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
			resized_image = cv2.resize(img, (100, 100))
			cv2.imwrite("neg/"+str(pic_num)+".jpeg", resized_image)
			pic_num+=1

		except Exception as e:
			print(str(e))
	for image in glob.glob("All/*.png"):
	

		if not os.path.exists('neg'):
			os.makedirs('neg')

		try:
			# print(i)
			# urllib.request.urlretrieve(i, "neg/"+str(pic_num)+'.jpg')
			img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
			resized_image = cv2.resize(img, (100, 100))
			cv2.imwrite("neg/"+str(pic_num)+".png", resized_image)
			pic_num+=1

		except Exception as e:
			print(str(e))


def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))


def create_pos_n_neg():
    for file_type in ['neg']:
        
        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

# store_raw_images_from_dir()
find_uglies()
create_pos_n_neg()
import streamlit as st
from PIL import Image 
from io import BytesIO 
import numpy as np 
import cv2
# function to convert an image to a 
# water color sketch 
def convertto_watercolorsketch(inp_img): 
	gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    
    # Apply a median blur to the grayscale image
	gray = cv2.medianBlur(gray, 5)
    
    # Detect edges in the image using adaptive thresholding
	edges = cv2.adaptiveThreshold(gray, 255, 
                                  cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, 9, 9)
    
    # Apply a bilateral filter to the original image
	color = cv2.bilateralFilter(inp_img, 9, 250, 250)
    # Combine the color image with the edges to get the cartoon effect
	cartoon = cv2.bitwise_and(color, color, mask=edges) 
	return cartoon

# function to convert an image to a pencil sketch 
def pencilsketch(inp_img): 
    gray_image = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    
    # Invert the grayscale image
    inverted_image = 255 - gray_image
    
    # Blur the inverted image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blurred = 255 - blurred
    
    # Create the pencil sketch image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    
    return pencil_sketch


# function to load an image 
def load_an_image(image): 
	img = Image.open(image) 
	return img 

# the main function which has the code for 
# the web application 
def main(): 
	imgs = Image.open("G:\Tooba\Intagram_Content\profilephoto.png")
	st.image(imgs, width = 400)
		# basic heading and titles 
	st.title('GUI BASED IMAGE CONVERSION') 
	st.write("Web application for converting\
	your ***image*** to a ***Water Color Sketch*** OR ***Pencil Sketch***") 

	st.subheader("Convert your image!") 
	st.warning("⚠ Only work on images")
	# image file uploader 
	image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"]) 

	# if the image is uploaded then execute these 
	# lines of code 
	if image_file is not None: 
		
		# select box (drop down to choose between water 
		# color / pencil sketch) 
		option = st.selectbox('How would you like to convert the image', 
							('water color sketch', 
							'pencil sketch')) 
		if option == 'water color sketch': 
			image = Image.open(image_file) 
			final_sketch = convertto_watercolorsketch(np.array(image)) 
			im_pil = Image.fromarray(final_sketch) 

			# two columns to display the original image and the 
			# image after applying water color sketching effect 
			tab1 , tab2 = st.tabs(["Water color", "Sketch"]) 
			with tab1: 
				st.header("Original Image") 
				st.image(load_an_image(image_file), width=250) 

			with tab2: 
				st.header("Water Color Sketch") 
				st.image(im_pil, width=250) 
				buf = BytesIO() 
				img = im_pil 
				img.save(buf, format="JPEG") 
				byte_im = buf.getvalue() 
				st.download_button( 
					label="Download image", 
					data=byte_im, 
					file_name="watercolorsketch.png", 
					mime="image/png"
				) 

		if option == 'pencil sketch': 
			image = Image.open(image_file) 
			final_sketch = pencilsketch(np.array(image)) 
			im_pil = Image.fromarray(final_sketch) 
			
			# two columns to display the original image 
			# and the image after applying 
			# pencil sketching effect 
			col1, col2 = st.columns(2) 
			with col1: 
				st.header("Original Image") 
				st.image(load_an_image(image_file), width=250) 

			with col2: 
				st.header("Pencil Sketch") 
				st.image(im_pil, width=250) 
				buf = BytesIO() 
				img = im_pil 
				img.save(buf, format="JPEG") 
				byte_im = buf.getvalue() 
				st.download_button( 
					label="Download image", 
					data=byte_im, 
					file_name="watercolorsketch.png", 
					mime="image/png")			
				
if __name__ == '__main__': 
	main() 

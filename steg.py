# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
import streamlit as st
from PIL import Image
import io

tab_1, tab_2,tab_3 = st.tabs(['Process Steganography','Encode Output','Decode Output'])

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

		# list of binary codes
		# of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode():
	img = st.sidebar.file_uploader("Input Image ")
	if img != None :
		image = Image.open(img, 'r')

		data = st.sidebar.text_input("Enter data to be encoded : ")
		tab_1.image(image, "cover image")
		if (len(data) == 0):
			st.warning("No data to encode")
		else :
			tab_1.success("Data to encode")
			tab_1.write(data)
		newimg = image.copy()
		
		encode_enc(newimg, data)
		def convert_image_to_bytes(img):
			img_bytes = io.BytesIO()
			img.save(img_bytes, format='PNG')
			return img_bytes.getvalue()
		
		image_bytes = convert_image_to_bytes(image)
		
		new_img_name = st.sidebar.text_input("Enter the name of new image(with extension) : ")
		if new_img_name != None :
			tab_2.download_button(label="Download Encoded Image",data= image_bytes,
						  file_name= f'{new_img_name}.png',mime= "image/png")
			#if download_img != None :
				#newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
	img = st.sidebar.file_uploader("Input Image to Decode ")
	if img != None :
		image = Image.open(img, 'r')
		tab_3.image(image= image, caption= "Image to decode")
		data = ''
		imgdata = iter(image.getdata())
		i = 0
		while (i < 1):
			pixels = [value for value in imgdata.__next__()[:3] +
									imgdata.__next__()[:3] +
									imgdata.__next__()[:3]]

			# string of binary data
			binstr = ''

			for i in pixels[:8]:
				if (i % 2 == 0):
					binstr += '0'
				else:
					binstr += '1'

			data += chr(int(binstr, 2))
			i += 1
			if (pixels[-1] % 2 != 0):
				
				return data

# Main Function
def main():
	option = st.sidebar.selectbox("Choose the action to perform in the application",('Encode','Decode'))
	if (option == "Encode"):
		encode()

	elif (option == "Decode"):
		tab_3.write("Decoded Word : " + decode())
		#data = decode()
		#if data != None :
			#tab_3.success("Image Decoded")
			#tab_3.subheader(data)
	else:
		raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :

	# Calling main function
	main()

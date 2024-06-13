import streamlit as st
from PIL import Image
import numpy as np
import io



def encode(image, message):
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Add delimiter indicating end of message
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Encode message into image
    index = 0
    for row in range(img_array.shape[0]):
        for col in range(img_array.shape[1]):
            for color in range(3):  # R, G, B channels
                if index < len(binary_message):
                    img_array[row][col][color] = img_array[row][col][color] & ~1 | int(binary_message[index])
                    index += 1
                else:
                    break
            if index >= len(binary_message):
                break
        if index >= len(binary_message):
            break
    
    encoded_image = Image.fromarray(img_array)
    
    return encoded_image

def decode(image):
    binary_message = ''
    img_array = np.array(image)
    
    # Decode message from image
    for row in range(img_array.shape[0]):
        for col in range(img_array.shape[1]):
            for color in range(3):  # R, G, B channels
                binary_message += str(img_array[row][col][color] & 1)
    
    # Find delimiter and extract message
    delimiter_index = binary_message.find('1111111111111110')
    if delimiter_index != -1:
        binary_message = binary_message[:delimiter_index]
        decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
        return decoded_message
    else:
        return "No message found"

def main():
    st.title("Steganography Tool")
    
    option = st.sidebar.selectbox("Choose the action", ('Encode', 'Decode'))
    
    if option == 'Encode':
        st.subheader("Encode Message")
        image = st.file_uploader("Upload Image", type=["jpg", "png"])
        message = st.text_area("Enter Message to Encode")
        
        if st.button("Encode"):
            if image is not None and message != "":
                encoded_image = encode(Image.open(image), message)
                st.image(encoded_image, caption="Encoded Image", use_column_width=True)
                
                # Enable users to download the encoded image
                img_bytes = io.BytesIO()
                encoded_image.save(img_bytes, format='PNG')
                st.download_button("Download Encoded Image", img_bytes.getvalue(), "encoded_image.png")
                
            else:
                st.warning("Please upload an image and enter a message to encode.")
    
    elif option == 'Decode':
        st.subheader("Decode Message")
        image = st.file_uploader("Upload Image to Decode", type=["jpg", "png"])
        
        
        if st.button("Decode"):
            if image is not None:
                st.image(image= image, caption= "Image to decode" )
                decoded_message = decode(Image.open(image))
                st.success("Decoded Message:")
                st.subheader(decoded_message)
            else:
                st.warning("Please upload an image to decode.")

if __name__ == '__main__':
    main()



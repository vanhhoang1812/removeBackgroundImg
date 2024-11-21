# importing modules
import streamlit as st
from rembg import remove
from PIL import Image, ImageColor
from io import BytesIO
import base64

# page configurations
st.title("Remove Background Image")

st.divider()
st.subheader("Upload an image :")
col0, col1, col2 = st.columns(3)
image = st.file_uploader(":arrow_up_small:  ", type=["png", "jpg", "jpeg"])


# Download the enhanced image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(image):
    image = Image.open(image)
    edited_img = remove(image)
    col0.write("Original")
    col0.image(image)

    col1.write("Remove Background")
    col1.image(edited_img)
    
    selected_color = None
    st.subheader("Select a Color of Your Choise :")
    selected_color = st.color_picker("Select Color",)
    st.download_button("Download :inbox_tray: ", convert_image(edited_img), "output.png", "image/png",key="1")
    # Replace background with selected color
    edited_img = edited_img.convert("RGBA")
    data = edited_img.getdata()

    new_image = []
    for item in data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            color_rgb = ImageColor.getrgb(selected_color)
            new_image.append((*color_rgb, 255))
        else:
            new_image.append(item)

    edited_img.putdata(new_image)

    col2.write("Background Color")
    col2.image(edited_img)
    st.download_button("Download with color :rainbow: ", convert_image(edited_img), "output.png", "image/png",key="2")

if image is not None:
    fix_image(image)
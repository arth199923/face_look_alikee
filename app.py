import streamlit as st
import requests
import base64
import random
import io
from PIL import Image

# Define your Segmind API key here
SegmindAPIKey = "SG_4ec6a76090edb729"

# Function to convert uploaded image to base64
def get_base64_image(uploaded_image):
    image = Image.open(uploaded_image)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Placeholder function for image caption
def get_image_caption(image):
    return "Placeholder caption for the uploaded image."

# Function to generate images using Segmind API
def generate_images(base64image, imagecaption, count):
    url = "https://api.segmind.com/v1/ssd-img2img"
    generated_images = []

    for i in range(count):
        currentseed = random.randint(1000, 1000000)

        # Prepare the request payload
        data = {
            "image": base64image,
            "prompt": imagecaption + ", stock photo",
        }

        # Send a POST request to the API
        response = requests.post(url, json=data, headers={'x-api-key': SegmindAPIKey})

        if response.status_code == 200 and response.headers.get('content-type') == 'image/jpeg':
            # Convert the image data to a PIL image
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            generated_images.append(image)

    return generated_images

# Function to process uploaded image and generate images
def process_image(uploaded_image, count):
    base64image = get_base64_image(uploaded_image)
    imagecaption = get_image_caption(uploaded_image)
    generated_images = generate_images(base64image, imagecaption, count)
    return imagecaption, generated_images

# Streamlit interface
def main():
    st.title("Discover Your Doppelgänger with AI, Crafted by Arth")
    st.markdown("📷 Upload your passport-style or similar photo to generate your look-alike")
    st.info("Please note: For faster results, upload a pic less than 500KB.")

    # Load sample image
    sample_image = Image.open("sample_upload.jpg")

    # Display sample image
    st.subheader("Here's a sample of uploaded and generated images:")
    st.image(sample_image, caption="Sample Image", use_column_width=True)

    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

    if uploaded_image is not None:
        count = st.selectbox("Number of Images", options=[1, 2, 3])
        
        if st.button("Generate Images"):
            imagecaption, generated_images = process_image(uploaded_image, count)

            st.text("AI Generated Caption:")
            st.text(imagecaption)

            # Display uploaded image on the left
            col1, col2 = st.columns(2)
            col1.subheader("Uploaded Image:")
            col1.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

            # Display generated images on the right
            col2.subheader("Generated Images:")
            for i, image in enumerate(generated_images):
                col2.image(image, caption=f"Generated Image {i+1}", use_column_width=True)

    # Note about potential API key limitations
    st.markdown("""
        **Note:** If you encounter issues with the application not generating images, 
        it could be due to the usage of a freely available API key, which may have reached its usage limit.
    """)

if __name__ == "__main__":
    main()

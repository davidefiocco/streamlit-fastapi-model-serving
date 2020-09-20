import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from PIL import Image
import io

# interact with FastAPI endpoint
url = 'http://fastapi:8000'
endpoint = '/segmentation'

def process(image, server_url: str):

    m = MultipartEncoder(
        fields={'file': ('filename', image, 'image/jpeg')}
        )

    r = requests.post(server_url,
                      data=m,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)

    return r

# construct UI layout

st.title('DeepLabV3 image segmentation')

st.write('''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation.''')  # description and instructions

input_image = st.file_uploader('insert image')  # image upload widget

if st.button('Get segmentation map'):

    if input_image is None:
        st.write("Insert an image!")  # handle case with no image
    else:
        segments = process(input_image, url+endpoint)
        segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
        st.image([input_image, segmented_image], width=300)  # output dyptich

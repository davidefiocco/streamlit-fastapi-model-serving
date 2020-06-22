import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from PIL import Image
import io

st.title('Image semantic segmentation')

# fastapi endpoint
url = 'http://fastapi:8000'
endpoint = '/segmentation'

st.write("This streamlit example uses a FastAPI service as backend. \n \
         Visit http://localhost:8000/docs for its swagger documentation")

image = st.file_uploader('insert image')  # image widget


def process(image, server_url: str):

    m = MultipartEncoder(
        fields={'file': ('filename', image, 'image/jpeg')}
        )

    r = requests.post(server_url,
                      data=m,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)

    return r


if st.button('Process'):
    segments = process(image, url+endpoint)
    segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
    st.image([image, segmented_image], width=300)

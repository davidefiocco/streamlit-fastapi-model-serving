import streamlit as st
from json import JSONDecodeError
import requests

st.title('Using Streamlit with a FastAPI backend')

url = 'http://fastapi:8000'
endpoint = '/compute'

st.write("This simple example uses as backend a FastAPI service. Visit http://localhost:8000/docs for its swagger documentation")

x = st.slider('x')  # a simple widget


def process(int: x, server_url: str):

    payload = {
        "number": x,
    }

    r = requests.post(server_url, json=payload)

    try:
        response = r.json()
        result = response['result']
    except JSONDecodeError:
        pass

    return result


st.write(x, 'after running through the API gives: ', process(x, url + endpoint))

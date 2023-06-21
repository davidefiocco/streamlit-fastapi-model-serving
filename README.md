# streamlit-fastapi-model-serving

Simple example of usage of streamlit and FastAPI for ML model serving described on [this blogpost](https://davidefiocco.github.io/streamlit-fastapi-ml-serving) and [PyConES 2020 video](https://www.youtube.com/watch?v=IvHCxycjeR0).

When developing simple APIs that serve machine learning models, it can be useful to have _both_ a backend (with API documentation) for other applications to call and a frontend for users to experiment with the functionality.

In this example, we serve an [image semantic segmentation model](https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/) using `FastAPI` for the backend service and `streamlit` for the frontend service. `docker compose` orchestrates the two services and allows communication between them.

To run the example in a machine running Docker and docker compose, run:

    docker compose build
    docker compose up

To visit the FastAPI documentation of the resulting service, visit http://localhost:8000/docs with a web browser.  
To visit the streamlit UI, visit http://localhost:8501.

Logs can be inspected via:

    docker compose logs

### Debugging

To modify and debug the app, [development in containers](https://davidefiocco.github.io/debugging-containers-with-vs-code) can be useful (and kind of fun!).

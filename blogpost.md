# Machine learning model serving in Python using FastAPI and streamlit

In my current job I train machine learning models. When experiments show that such models can solve some company need, we often serve them to users in the form of "prototypes" deployed on internal servers. While such prototypes may not be production-ready yet, they are very useful to show to users the capabilities and limitations of the models and get feedback and release better iterations.

Often these prototypes need to have:
1. a frontend (a user interface aka UI), so that people can use and evaluate if the model works well enough to be useful;
2. a backend with API documentation, so they can be moved easily to production and integrated with other applications later on. 

Also, it'd be nice to create these easily, quickly and concisely, so that more attention and time can be devoted to better data and model development!

In the recent past I have dabbled in HTML and Javascript to create UIs, and used Flask to create the underlying backend services. This did the job, but:

- I could just create very simple UIs (using [bootstrap](https://getbootstrap.com/) and [jQuery](https://jquery.com/)), but had to bug my colleagues to make them functional and not totally ugly.
- My Flask API endpoints were very simple, they didn't have documentation. They also served results using the server built-in Flask which is [not suitable for production](https://flask.palletsprojects.com/en/1.1.x/deploying/).

### What if both frontend and backend could be easily built with (little) Python?

You may already have heard of FastAPI and streamlit, two Python libraries that lately are getting quite some attention in the applied ML community. 

[FastAPI](https://fastapi.tiangolo.com/) is [gaining popularity](https://twitter.com/honnibal/status/1272513991101775872) as Python framework. It is thoroughly documentation, allows to code APIs following [OpenAPI specifications](https://en.wikipedia.org/wiki/OpenAPI_Specification) and can use `uvicorn` behind the scenes, allowing to make it "good enough" for some production use. Its syntax is also similar to that of Flask, so that its easy to switch to it if you have used Flask before.

[streamlit](https://www.streamlit.io/) is [getting traction](https://twitter.com/streamlit/status/1272892481470857232?s=20) as well. It allows to create pretty complex UIs in pure Python. It can be used to serve ML models without further ado, but (as of today) [you can't build REST endpoints with it](https://github.com/streamlit/streamlit/issues/439).

So why not combine the two, and get the best of both worlds?

## A simple "full-stack" application: image semantic segmentation with DeepLabV3

As an example, let's take *image segmentation*, which is the task of assigning to each pixel of a given image to a category (for a primer on image segmentation, check out the [fast.ai course](https://course.fast.ai/videos/?lesson=3)).  
Semantic segmentation can we done using pre-trained models (like [DeepLabV3](https://arxiv.org/pdf/1706.05587.pdf)) on a predefined list of categories, and these have been already [implemented in PyTorch](https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/). 
How can we serve those in an a app with a streamlit frontend and FastAPI backend?

One possibility is to have two services deployed in two Docker containers, orchestrated with `docker-compose`. The `streamlit` service serves a UI that calls (using the `requests` package) the endpoint exposed by the `fastapi` service:

```yml
version: '3'

services:
  fastapi:
    build: fastapi/
    ports: 
      - 8000:8000
    networks:
      - deploy_network
    container_name: fastapi

  streamlit:
    build: streamlit/
    depends_on:
      - fastapi
    ports: 
        - 8501:8501
    networks:
      - deploy_network
    container_name: streamlit

networks:
  deploy_network:
    driver: bridge
```


# Machine learning model serving in Python using FastAPI and streamlit

In my current job I train machine learning models. When experiments show that such models can solve some company need, we often serve them to users in the form of "prototypes" deployed on internal servers. While such prototypes may not be production-ready yet, they are very useful to show to users the capabilities and limitations of the models and get feedback and release better iterations.

Ideally these prototypes should have two features:
1. a frontend (a user interface aka UI), so that people can use and evaluate if the model works well enough to be useful;
2. a backend with API documentation, so they can be moved easily to production and integrated with other applications later on. 

Also, it'd be nice to accomplish all of the above easily, quickly and concisely, so that more time can be devoted to better data and model development! ;)

In the recent past I have dabbled in HTML and Javascript to create UIs, and used Flask to create the underlying backend services. This did the job, but:

- I could just create very simple UIs (using bootstrap and jQuery) and needed help from my patient colleagues to make them functional and not completely horrible.
- My Flask API endpoints were very simple, they didn't have documentation. They also served results using the server built-in Flask which is [not suitable for production](https://flask.palletsprojects.com/en/1.1.x/deploying/).

### What if both frontend and backend could be easily built with (little) Python?

You may already have heard of FastAPI and streamlit, two Python libraries that lately are getting quite some attention in the applied ML community. 

[FastAPI](https://fastapi.tiangolo.com/) is [gaining popularity](https://twitter.com/honnibal/status/1272513991101775872) as Python framework. It is thoroughly documentation, allows to code APIs following [OpenAPI specifications](https://en.wikipedia.org/wiki/OpenAPI_Specification) and can use `uvicorn` behind the scenes, allowing to make it "good enough" for some production use. Its syntax is also similar to that of Flask, so that its easy to switch to it if you have used Flask before.

[streamlit](https://www.streamlit.io/) is [getting traction](https://twitter.com/streamlit/status/1272892481470857232?s=20) as well. It allows to create pretty complex UIs in pure Python. It can be used to serve ML models without further ado, but (as of today) [you can't build REST endpoints with it](https://github.com/streamlit/streamlit/issues/439).

So why not combine the two, and get the best of both worlds?

### A simple "full-stack" application: image semantic segmentation with Deeplab

To have streamlit working on top of FastAPI, one possibility is to have two services deployed in two Docker containers, orchestrated with `docker-compose`. The `streamlit` service serves a UI that calls (using the `requests` package) the endpoints of the `fastapi` service:


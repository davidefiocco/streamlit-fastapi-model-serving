# Fullstack ML model serving in Python using FastAPI and streamlit

In my current job I train machine learning models. When models prove to be useful "in the lab" to solve some of the company needs, we often serve them to users in the form of prototypes. While such prototypes may not be production-ready yet, they are very useful to show to users the capabilities and limitations of our models and get their feedback so to improve them further.

It's desirable for these prototypes to have two features:
1. have a frontend so that people can use and evaluate if the model works well enough to be useful;
2. have a backend with API documentation so they can be moved easily to production and integrate with other applications later on. 

Of course, I would like to accomplish all of the above quickly, so that more time can be devoted to better data and model development! :)

In the recent past I have dabbled in HTML and Javascript to create a UI, and used Flask to create REST services. This did the job, but:

- I could just create very simple UIs (using bootstrap and jQuery) and needed help from colleagues to make them functional and not completely horrible.
- My Flask API endpoints were very simple, they didn't have documentation and used its built-in server which is [not suitable for production](https://flask.palletsprojects.com/en/1.1.x/deploying/).

### What if both frontend and backend could be easily built with (little) Python?

Python libraries that are getting attention in the applied ML community lately are FastAPI and streamlit. 

[FastAPI](https://fastapi.tiangolo.com/) is [gaining popularity](https://twitter.com/honnibal/status/1272513991101775872) as Python framework and has extensive documentation, allows to code APIs following [OpenAPI specifications](https://en.wikipedia.org/wiki/OpenAPI_Specification) and can use `uvicorn` behind the scenes, allowing to make it "good enough" for some production use. Its syntax is also similar to that of Flask, so that its easy to switch to it if you have used Flask before.

[streamlit](https://www.streamlit.io/) also is [getting traction](https://twitter.com/streamlit/status/1272892481470857232?s=20) and allows to create complex UIs in pure Python. It can be used to serve ML models without further ado, but (as of today) [you can't build REST endpoints with it](https://github.com/streamlit/streamlit/issues/439).

So why not combine the two, and get the best of both worlds?

### A simple "full-stack" application

To get FastAPI work together with streamlit, one idea is to have two services deployed in two Docker containers, orchestrated with `docker-compose`. The "streamlit" service serves a UI that calls (using the `requests` package) the endpoints of the FastAPI service:


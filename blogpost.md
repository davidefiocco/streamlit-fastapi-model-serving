# Fullstack ML model serving in Python using FastAPI and streamlit

In my current job I train machine learning models. When models prove to be useful "in the lab" to solve some of the company needs, we often serve it to users in the form of prototypes. Such prototypes may not be production-ready yet, but are useful to show to users the capabilities and limitations of our models and get their feedback so to improve them further.

It's desirable for these prototypes to have two features:
1. have a frontend so that people can use and evaluate if the model works well enough to be useful;
2. have a backend with API documentation, so that if they prove useful, they can be moved easily to production and integrate with other applications. 

Of course, I would like to accomplish all of the above quickly, so that more time can be devoted to better data and model development :)

### What if frontend and backend could be both easily built with (little) Python?

In the recent past I have dabbled in HTML and Javascript to create a UI, and used Flask to create a simple REST service. This did the job, but:

- I could just create very simple UIs (using bootstrap and jQuery) and needed a help from colleagues to create something usable and not completely horrible.
- My Flask API endpoints were very simple, they didn't have documentation and used its built-in server, which is [not suitable for production](https://flask.palletsprojects.com/en/1.1.x/deploying/).

Python libraries that are getting attention in the applied ML community lately are [FastAPI](https://fastapi.tiangolo.com/) and [streamlit](https://www.streamlit.io/). 

FastAPI is [gaining popularity](https://twitter.com/honnibal/status/1272513991101775872) as Python framework and has extensive documentation, allows to code APIs following [OpenAPI specifications](https://en.wikipedia.org/wiki/OpenAPI_Specification) and can use `uvicorn` behind the scenes, allowing to make it "good enough" for some production use, its syntax is similar to Flask so that its easy to switch to it.

streamlit also is [getting traction](https://twitter.com/streamlit/status/1272892481470857232?s=20) to create complex UIs in pure Python.  

So why not combine the two?

### A simple "full-stack" application

To get FastAPI work together with streamlit, one idea is to have two services deployed in two Docker containers, orchestrated with `docker-compose`. The "FastAPI" service contains the model, and the "streamlit" service serves a UI that calls (using the `requests` package) the endpoints of the FastAPI container:


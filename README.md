# Langchain

## How are we using Langchain?
We built a flask server that makes use of langchain framework to interact with openai. Thus, instead of directly sending HTTP requests
to openai API, we send requests to langchain flask server which forwards these requests to openai API. 

HTTP Request: amotions-web -> langchain flask server API -> openai API
<br />
HTTP Response: openai API -> langchain flask server API -> amotions-web

## How was langchain server created?
I will break this into three parts, in each I will talk about a file in the repo.

1. ingestion.py
In this file, we simply upload data (e.g books pdfs), then we split the data semantically into small chunks, and then we upload these data chunks to the vector database called Pinecone. Pinecone stores these chunks in a smart way by converting text chunks into vectors (vector is a list of numbers) using mathematical equations which we don't care about, but it does the job. textchunks -> vectors. After this file has finished running, the data will be stored in a Pinecone vector store which is hosted on the cloud. Now, that we have our data on the cloud in the form of vectors, we can use them. Meaning, we need to run ingestion only when we upload new data. Note: Duplicate data will be ignored, so don't worry about running ingestion file mutiple times if you did.

2. backend/core.py
In this file, we chat with the data stored on Pinecone by sending it questions. The way this works is that when we send a question to the Pinecone vector store, Pinecone searches for vectores in the store that are semantically relevant to the question and returns these data vectors to us with the question as a single query - query = question + vectors->text->context. We now have the question + context from the data we uploaded to Pinecone. Finally we can send this query=(question+context) to openai, which will use the context and its general data to answer your question and resopnd with the answer as a json object.

3. application.py
In this file, we build the api that trigers core.py whenever a POST HTTP requests is sent to our server with the param query="Question". After core.py function has returend the answer to the question, we send an HTTP response with the answer as json object.

## How was langchain hosted?
1. Created a virtual environment to build the server
2. Created a git repo and pushed it to github
3. Created the requirements.txt file by running ```pip freeze -> requirements.txt```. This makes sure that the production environment will have all the packages you have locally on your machine, so make sure to run this command every time you install new packages using the pip command 
4. Created YAML file and named it main.yml to inform the production environment of what commands need to be run to build the code.
5. Created AWS codePipline and codebuild for CI/CD
6. Created AWS Elastic Beanstalk to host the falsk server

## Pull and Make Changes:
1. Clone the repository 
2. Create you own branch
3. Create a virtual environment. I used pipenv - ```pipenv shell``` in root directory . You can use whatever you like to create your virtual env
4. Install the requirements dependencies/packages by running ```pip install -r requirements.txt```
5. Make changes and test locally before pushing to remote
6. run command: python application.py
7. Server should be running on your localhost, use the url given in the terminal to test with Postman
8. If everything is working correctly, then you can move to the next step
9. If you have installed any packages using the command ```pip install package_name```, make sure you are in the virtual environment, then run the command pip freeze -> requirements.txt. This command will update the requirements.txt for production environment
10. You are ready to push now, commit your changes and push them to your branch. NOTE: Follow the instruction in amotions-web repo readme for how to merge and release new feature to production.

### If you have any question or need help, please ask in slack.

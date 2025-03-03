# searchagent
## About
This repository contains a simple implementation of an agent-powered chatbot built with [smolagents](https://github.com/huggingface/smolagents) and Streamlit. The chatbot is able to use a search engine, visit web pages, and search wikipedia in order to form responses. This allows access to real-time information and other sources not otherwise available at training time.

## Demo
Visit the [live demo](https://searchagent-7zcnbnvqndoyrvho5ebt6w.streamlit.app/). 

## Usage
Run the Streamlit application locally with the following command:
```
make run-app
```

Run a single query:
```
make run-query QUERY="What is the current date?"
```
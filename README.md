# Repo Chat

Repo Chat is a service that allows you to interact with your own code repository (placed as sibling directories) via the GPT-3.5 and GPT-4 models by OpenAI through a web interface (http://repochat.localhost:8008/). It utilizes Docker and FastAPI to create a lightweight and portable application. Repo Chat is designed to be used in a development environment where the codebase is constantly changing. It uses the LangChain library to process the codebase and generate contextual embeddings that are then used as input to your selected OpenAI chat model.

## Description

The main functionality of Repo Chat is contained within the `./repochat` directory. It features two main endpoints: one for asking questions and another for scanning and uploading the context from the codebase.

The `/ask_question` endpoint allows you to interact with the GPT-3.5 / GPT-4 model. You can pass your question as a parameter and the service will return a response from the model. The `/scan_upload` endpoint is used to process the codebase and generate the contextual embeddings. It scans all sibling directories of the `./repochat` directory, thanks to the Docker volume configuration `.:/app`.

Repo Chat also keeps a log of all the interactions with the chat model. These logs are saved in markdown format, grouped by the day of interaction. This allows for easy reviewing and debugging of the chat history by the end-user. They are also saved locally into a .json file, which the code itself uses rather than the user-friendly.md files.

## Prerequisites

To use Repo Chat, you need to have Docker and Docker Compose installed on your machine. You can find the installation instructions for Docker [here](https://docs.docker.com/get-docker/), and for Docker Compose [here](https://docs.docker.com/compose/install/).

## Installation & Usage

To use Repo Chat, you need to build and start the Docker containers. You can do this with the following command:

```bash
docker-compose up --build
```

After running this command, you can use the following URLs to interact with the service:

- Ask questions: http://repochat.localhost:8008/
- Scan upload: http://repochat.localhost:8008/docs#/default/rescan_repo_upload_context_scan_upload_post

You may need to restart the `repochat` service after running the `scan_upload` endpoint. You can do this with the command `docker-compose restart repochat`.

The idea is that you will place repochat into your own repository, so that it can pull in all sibling directories.

## API Documentation

The API documentation is automatically generated and can be accessed at http://repochat.localhost:8008/docs. Here, you can find more detailed instructions and examples for each endpoint.

## Limitations and Considerations

Please note that the number of tokens you can pass to the GPT-3.5 model is limited (~16k) and the GPT-4 model is also limited (~8k). Therefore, you cannot pass the entire repository as context. To work around this, Repo Chat allows you to control the chat history and the number of contextual documents passed to the model using a two-pass filtering system.

Additionally, while the chat logs provide a convenient way to review the chat history, they may not be suitable for large-scale or long-term storage of chat data. For such use cases, consider implementing a more robust data storage solution.

## Future Work

In the future, we plan to add more features to Repo Chat, such as supporting different models, improving the context selection algorithm, and providing more advanced chat history management options. Stay tuned for updates! And please feel free to contribute to this project.
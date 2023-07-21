import json
import os
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from repochat.ask_questions import ask_questions
from repochat.scan_upload import run_index

app = FastAPI()
templates = Jinja2Templates(directory="./repochat/templates")

# Define the path to the chat history JSON file
chat_history_file = "./repochat/chat_logs/chat_history.json"


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask_question")
async def ask_question(request: Request):
    global chat_history_file
    form = await request.form()
    question = form.get("question")

    # First Layer of path filters
    path_filter_layer_1 = form.get("path_filter_layer_1")
    path_filter_layer_1 = path_filter_layer_1.split(",")
    path_filter_layer_1 = [x.strip() for x in path_filter_layer_1]
    if path_filter_layer_1 == [""]:
        path_filter_layer_1 = []

    # Second Layer of path filters
    path_filter_layer_2 = form.get("path_filter_layer_2")
    path_filter_layer_2 = path_filter_layer_2.split(",")
    path_filter_layer_2 = [x.strip() for x in path_filter_layer_2]
    if path_filter_layer_2 == [""]:
        path_filter_layer_2 = []

    # checkboxes
    gpt4_on = form.get("gpt4_on", False)
    test_mode = form.get("test_mode", False)
    pass_chat_history = form.get("pass_chat_history", 3)

    # convert values to boolean
    gpt4_on = gpt4_on == "true"
    test_mode = test_mode == "true"
    pass_chat_history = int(pass_chat_history)

    chat_history = await ask_questions(
        [question],
        gpt4_on,
        chat_history_file,
        test_mode,
        pass_chat_history,
        path_filter_layer_1,
        path_filter_layer_2,
    )
    qa = chat_history[-1]
    answer = qa["answer"]
    # answer = "This is the answer to your question."
    return templates.TemplateResponse(
        "index.html", {"request": request, "answer": answer, "form_data": form}
    )


@app.post("/questions")
async def handle_questions(
    questions: List[str],
    gpt4_on: bool = False,
    test_mode: bool = False,
    pass_chat_history: int = 3,
    path_filter_layer_1: List[str] = [],
    path_filter_layer_2: List[str] = [],
):
    global chat_history_file
    chat_history = await ask_questions(
        questions,
        gpt4_on,
        chat_history_file,
        test_mode,
        pass_chat_history,
        path_filter_layer_1,
        path_filter_layer_2,
    )
    return chat_history


@app.post("/scan_upload")
async def rescan_repo_upload_context():
    result = await run_index()
    if result == 0:
        return "success"
    else:
        return "failure"

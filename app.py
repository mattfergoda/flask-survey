from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def render_home_page():
    return render_template("survey_start.html", survey=survey)

@app.post("/begin")
def begin_page_redirect():
    return redirect('/question/0')

@app.get("/question/<int:question_id>")
def question_page(question_id):
    if question_id < len(survey.questions):
        return render_template("question.html", question = survey.questions[question_id])
    else:
        return render_template("completion.html")

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
    """Renders Home page"""

    return render_template("survey_start.html", survey=survey)


@app.post("/begin")
def begin_page_redirect():
    """Redirects from the '/begin' endpoint to question 0"""

    """ global responses """
    responses.clear()

    return redirect('/question/0')


@app.post("/answer")
def anwser_page_redirect():
    """takes a question_id. Routes to anwser page for question. Appends
    response to response list. Redirects to next question"""

    responses.append(request.form["answer"])

    return redirect(f"/question/{len(responses)}")


@app.get("/question/<int:question_id>")
def question_page(question_id):
    """Takes a question_id. Renders either next question or completion page."""

    if question_id < len(survey.questions):

        return render_template("question.html", question=survey.questions[question_id], question_id=question_id+1)
    else:

        return render_template("completion.html", survey=survey, responses=responses)

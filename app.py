from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
SESSION_KEY = "responses"
SURVEY_CODE_KEY = "survey_code"


@app.get("/")
def render_home_page():
    """Renders Home page"""

    return render_template("survey_start.html", surveys=surveys)


@app.post("/begin")
def begin_survey():
    """Clears session responses to begin survey.
    Redirects from the '/begin' endpoint to question 0"""

    session[SESSION_KEY] = []
    session[SURVEY_CODE_KEY] = request.form[SURVEY_CODE_KEY]

    return redirect('/question/0')


@app.post("/answer")
def handle_question():
    """takes a question_id. Routes to anwser page for question. Appends
    response to response list. Redirects to next question"""

    responses = session[SESSION_KEY]
    responses.append(request.form["answer"])
    session[SESSION_KEY] = responses

    return redirect(f"/question/{len(session[SESSION_KEY])}")


@app.get("/question/<int:question_id>")
def question_page(question_id):
    """Takes a question_id. Renders either next question or completion page."""
    next_question_id = len(session[SESSION_KEY])
    questions = surveys[session[SURVEY_CODE_KEY]].questions
    if next_question_id == len(questions):
        return redirect("/complete")
    elif question_id != next_question_id:
        flash("ANSWER THEM IN ORDER")
        return redirect(f"/question/{next_question_id}")

    return render_template("question.html", question=questions[next_question_id])


@app.get("/complete")
def completion_page():
    """
    If the user has answered all the questions, render the completion page.
    Otherwise, redirect to the next question.
    """

    next_question_id = len(session[SESSION_KEY])
    # TODO: Swap Logic
    if next_question_id != len(surveys[session[SURVEY_CODE_KEY]].questions):
        return redirect(f"/question/{next_question_id}")

    return render_template("completion.html", survey=surveys[session[SURVEY_CODE_KEY]])

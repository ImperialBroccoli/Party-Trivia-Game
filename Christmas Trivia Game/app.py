from flask import Flask, render_template, redirect, url_for, request, jsonify, Response
import time

clicks = 0

app = Flask(__name__)

# Load questions and answers from files
with open("questions.txt", "r", encoding="utf-8") as qf, open("answers.txt", "r") as af:
    questions = qf.read().strip().split("\n")
    answers = af.read().strip().split("\n")

current_index = {"index": 0}  # Shared state for the current question index


@app.route("/")
def index():
    """Host view to display the current question."""
    return render_template("index.html")


@app.route("/current-question")
def current_question():
    """Endpoint for server-sent events (SSE) to send the current question."""
    def stream():
        while True:
            idx = current_index["index"]
            if idx < len(questions):
                question_with_br = questions[idx].replace("\\n", "<br>")
                yield f"data: {question_with_br}\n\n"
            else:
                yield "data: No more questions!\n\n"
            time.sleep(1)  # Stream updates every second
    return Response(stream(), content_type="text/event-stream")



@app.route("/secret", methods=["GET", "POST"])
def secret():
    """Controller view to show the answer and navigate to the next question."""
    idx = current_index["index"]
    if request.method == "POST":
        # Move to the next question
        if idx < len(questions) - 1:
            current_index["index"] += 1
        return redirect(url_for("secret"))

    # Show the current answer
    if idx < len(answers):
        answer = answers[idx]
    else:
        answer = "No more answers!"
    
    if answer == "BLANK":
        answer = ""
        
    return render_template("secret.html", answer=answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True) 
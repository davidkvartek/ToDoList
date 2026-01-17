# app.py
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
todos = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        todos.append(request.form["todo"])
        return redirect("/")
    return render_template_string("""
        <h1>To-Do List</h1>
        <form method="post">
            <input name="todo" placeholder="Add a to-do">
            <button type="submit">Add</button>
        </form>
        <ul>
            {% for todo in todos %}
                <li>{{ todo }}</li>
            {% endfor %}
        </ul>
    """, todos=todos)

if __name__ == "__main__":
    app.run(debug=True)

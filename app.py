from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.String(10), nullable=True) # YYYY-MM-DD
    priority = db.Column(db.Integer, default=1) # 1=Low, 2=Medium, 3=High

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("todo")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        
        if title:
            # Convert priority to int, default to 1 (Low)
            try:
                priority = int(priority)
            except (ValueError, TypeError):
                priority = 1
                
            new_todo = Todo(title=title, due_date=due_date, priority=priority)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('main.index'))
    
    # Sort by: Incomplete first, then Priority (High to Low), then Due Date (Soonest first)
    todos = Todo.query.order_by(
        Todo.complete.asc(), 
        Todo.priority.desc(), 
        Todo.due_date.asc().nullslast()
    ).all()
    
    return render_template("index.html", todos=todos)

@main.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.index'))

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

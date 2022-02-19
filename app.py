from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(120))

@app.route("/", methods=['GET', 'POST'])
def index():
    data = db.session.query(Todo).all()
    return render_template("homepage.html", todos=data)

@app.route("/add/todo", methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("homepage.html")

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete_todo(id):
    todo = db.session.query(Todo).filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update_todo(id):
    data = Todo.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        data.title = title
        data.description = description
        db.session.commit()
        return redirect("/")
    else:
        return render_template("update.html", todo=data)

if __name__ == "__main__":
    app.run(debug=True) 
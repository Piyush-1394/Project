from time import strftime
from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 
db = SQLAlchemy(app)

class Todo(db.Model):



    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        
        return f"{self.sno} - {self.title}"
    

@app.route("/", methods=['GET', 'POST'])
   
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)



@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return  'This is a todo list page'

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):

    todo = Todo.query.filter_by(sno=sno).first()

    if not todo:
        abort(404, description="Todo not found")

    
    if request.method == 'POST':
        # todo = Todo.query.filter_by(sno=sno).first()
        # date_created = Todo.query.filter_by(date_created=todo.date_created|strftime('%Y-%m-%dT%H:%M') )
        title = request.form['title']
        desc = request.form['desc']
        date_created = request.form['time']
        

        if date_created:
            parsed_date = datetime.strptime(date_created, '%Y-%m-%dT%H:%M')
            todo.date_created = parsed_date  # Store as datetime object

        todo.title = title
        todo.desc = desc
       
        db.session.commit()
        return redirect("/")

    formatted_date = (
        todo.date_created.strftime('%Y-%m-%dT%H:%M') if todo.date_created else ''
    )

    # todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo, formatted_date=formatted_date)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:
        abort(404, description="Todo not found")
    db.session.delete(todo)
    db.session.commit()
    return redirect("/") 

@app.route("/deleteall")
def delete_all():
    Todo.query.delete()
    db.session.commit()
    return "All todos deleted successfully!"
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



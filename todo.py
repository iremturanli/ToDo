from flask import Flask,render_template,redirect,url_for
from  flask_sqlalchemy import SQLAlchemy
from flask import request

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////home/turkai/Masaüstü/workplace/Flask/todolist/todolist/db/todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 


db=SQLAlchemy(app)

@app.route("/")
def index():
    
    todos=Todo.query.all()#sözlük yapısında "id":1,"title":"Deneme1"
    return render_template("index.html",todos=todos)



@app.route("/add",methods=["POST"])#get request'e izin verilmedi sadece post
def addTodo():
    title=request.form.get("title")
    content=request.form.get("content")
    newTodo=Todo(title=title,content=content,complete=False)#yapılacakseyler
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/complete/<string:id>",methods=["GET"])
def completeTodo(id):

    todo=db.session.query(Todo).filter(Todo.id==id).first()
    
    if todo.complete==False:
        todo.complete=True

    else:
        todo.complete=False

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo=db.session.query(Todo).filter(Todo.id==id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80))
    content= db.Column(db.Text)
    complete=db.Column(db.Boolean)


db.create_all()


if __name__=="__main__":
    app.run(debug=  True)

 

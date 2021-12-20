from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yourUsername:yourPassword@localhost:5432/flask_to_do'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), unique=True, nullable=False)
    isComplete = db.Column(db.Boolean)

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "task", "isComplete")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

class TodoListResource(Resource):
    def get(self):
        todos = Todo.query.all()
        return todos_schema.dump(todos)

    def post(self):
        new_todo = Todo(
            title=request.json['title'],
            content=request.json['content']
        )
        db.session.add(new_todo)
        db.session.commit()
        return todo_schema.dump(new_todo)

@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(TodoListResource, '/posts')

if __name__ == '__main__':
    app.run(debug=True)


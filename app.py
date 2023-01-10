
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin







app = Flask(__name__)
CORS(app,support_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:myDBpost@localhost/Testhere'

db = SQLAlchemy(app)



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)    

    def __repr__(self):
        return f"Event: {self.description}"

    def __init__(self,description):
        self.description = description

def format_event(event):
    return{
        "id" : event.id,
        "description" : event.description,
        "created_at" : event.created_at
    }    

@app.route("/events", methods = ["POST"])
@cross_origin(supports_credentials=True)
def create_event():
    description = request.json["description"]
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)


@app.route("/events", methods = ["GET"])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {"event" : event_list}



@app.route("/events/<id>", methods = ["GET","DELETE", "PUT"])
        
def single_events(id):
    
    if request.method == "GET":
        events = Event.query.filter_by(id = id).one()
        formated_event = format_event(events)
        return {"event" : formated_event}
    elif request.method == "DELETE":
        event = Event.query.filter_by(id = id).one()
        db.session.delete(event)
        db.session.commit()
        return f"event {id} deleted"

    elif request.method == "PUT":
        event = Event.query.filter_by(id = id)
        description = request.json["description"]
        event.update(dict(description = description, created_at = datetime.utcnow()))
        db.session.commit()
        return f"event {id} updated"



@app.route ("/")
def hello():
    return "Hey man"




if __name__ == "__main__":
    app.run(debug=True)


# from project_name import app, db
# app.app_context().push()
# db.create_all()
# . venv/bin/activate 
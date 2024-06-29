from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
@app.route("/")
def index():
    return "<h1>Hello, World!</h2>"

@app.route('/messages',methods=["GET","POST"])
def messages():
    if request.method=="GET":  
        messages=[message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        response=make_response(jsonify(messages),200)
        return response
    elif request.method=="POST":
        new_message=Message(
            body=request.form.get('body'),
            username= request.form.get('username')
            
        )
        db.session.add(new_message)
        db.session.commit()
        response=make_response(new_message.to_dict(),201)
        return response
        
        
    
@app.route('/messages/<int:id>',methods=["GET","PATCH","DELETE"])
def messages_by_id(id):
    
    message=Message.query.filter(Message.id==id).first()
    if message is None:
        response=make_response(jsonify({"error":"Message not found"}),404)
        return response
    else:
        if request.method=="GET":
            response=make_response(message.to_dict(),200)
            return response
        elif request.method=="PATCH":
            for attr in request.form:
                setattr(message,attr,request.form.get(attr))
            db.session.add(message)
            db.session.commit()
            response=make_response(jsonify(message.to_dict()),200)
            return response
        elif request.method=="DELETE":
            db.session.delete(message)
            db.session.commit()
            response=make_response(jsonify({"message":"Message deleted successfully"}),204)
            return response
        
    

if __name__ == '__main__':
    app.run(port=5555)

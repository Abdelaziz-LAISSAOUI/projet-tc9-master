from Carweb import app
from Carweb.models import *
from Carweb import db, ma 
from flask import Flask , jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_filter import query_with_filters

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


user_schema = UserSchema()
users_schema= UserSchema(many=True)



annonce_schema = AnnonceSchema()
annonce_schema = AnnonceSchema(many=True)

# *************************** START CRUD
@app.route("/cars")
def getAllCars():
    all_cars = Car.query.all()
    cars = cars_schema.dump(all_cars)
    return jsonify(cars)

@app.post("/annonce/new-annoncement/new-car")
@jwt_required()
def createannonce():
    current_user = get_jwt_identity()
    isLogged = jsonify(logged_in_as=current_user), 200
    if isLogged:
        title = request.json['title']
        name = request.json['name']
        car_Brand = request.json['car_Brand']
        price = request.json['price']
        fuel = request.json['fuel']
        seats = request.json['seats']
        region = request.json['region']
        year = request.json['year']
        kilos = request.json['kilos']
        desciption = request.json['desciption']
        new_car= Car(
            title,
            name,
            car_Brand,
            price,
            fuel,
            seats,
            region,
            year,
            kilos,
            desciption
        )
        db.session.add(new_car)
        db.session.commit()
        
        idOwner = request.json["owner_id"] #the body is here
        idCar = new_car.id

        new_annonce= Annonce(idCar, idOwner)
        db.session.add(new_annonce)
        db.session.commit()

        return annonce_schema.jsonify(new_annonce)

#       return annonce_schema.jsonify(new_car)

# @app.post("/annonce/new-annoncement/")
# @jwt_required()
# def createannonce():
#     current_user = get_jwt_identity()
#     if current_user:

@app.get("/annonce/<id>")
@jwt_required()
def getAnnonce(id):
    current_user = get_jwt_identity()
    if current_user:
        annonce = Annonce.query.get(id)
        return annonce_schema.jsonify(annonce)

@app.get("/user/<id>")
@jwt_required()
def getUser(id):
    current_user = get_jwt_identity()
    if current_user:
        user = User.query.get(id)
        return user_schema.jsonify(user)    

@app.put("/annonce/<id>")
@jwt_required()
def updateCar(id):
    current_user = get_jwt_identity()
    if current_user:
        annonce= Annonce.query.get(id) 
        carid= annonce.Car_id
        car= Car.query.get(carid)

        name = request.json['name']
        price = request.json['price']
        year = request.json ['year']

        car.name = name
        car.price = price
        car.year = year
        db.session.commit()

        return car_schema.jsonify(car)

@app.put("/user/<id>")
@jwt_required()
def updateUser(id):
    current_user = get_jwt_identity()
    if current_user:
        user= User.query.get(id)

        name = request.json['name']
        region = request.json['region']
        phone = request.json['phone_number']
        image = request.json['image']


        user.name = name
        user.region = region
        user.phone_number = phone
        user.image= image
        db.session.commit()

        return car_schema.jsonify(user)

def deleteCar(id): #TODO: delete car too
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    return car_schema.jsonify(car)
@app.delete("/annonce/<id>")
@jwt_required()
def deleteAnnonce(id):
    current_user = get_jwt_identity()
    if current_user:
        annonce = Annonce.query.get(id)
        carid= annonce.Car_id
        deleteCar(carid)
        db.session.delete(annonce)
        db.session.commit()
        return annonce_schema.jsonify(annonce)
# *************************** END CRUD


#**************************** START FILTRAGE
@app.route('/annonce/car/<title>', methods=['POST'])
def title_search():
    cars = query_with_filters(Car, request.json.get("title"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<name>', methods=['POST'])
def name_search():
    cars = query_with_filters(Car, request.json.get("name"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<Car_Brand>', methods=['POST'])
def brand_search():
    cars = query_with_filters(Car, request.json.get("Car_Brand"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<price>', methods=['POST'])
def price_search():
    cars = query_with_filters(Car, request.json.get("price"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<fuel>', methods=['POST'])
def fuel_search():
    cars = query_with_filters(Car, request.json.get("fuel"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<seats>', methods=['POST'])
def seats_search():
    cars = query_with_filters(Car, request.json.get("seats"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<region>', methods=['POST'])
def region_search():
    cars = query_with_filters(Car, request.json.get("region"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<year>', methods=['POST'])
def pet_search():
    cars = query_with_filters(Car, request.json.get("year"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<kilos>', methods=['POST'])
def pet_search():
    cars = query_with_filters(Car, request.json.get("kilos"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200

@app.route('/annonce/car/<description>', methods=['POST'])
def pet_search():
    cars = query_with_filters(Car, request.json.get("description"), CarsSchema)
    return jsonify(car_schema.dump(cars)), 200
#**************************** END FILTRAGE

#**************************** START SEARCH BAR
#**************************** END SEARCH BAR


#**************************** START REGISTER
from Carweb.form import*
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
                                email_address=form.email_address.data,
                                password=form.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)
        access_token = create_access_token(identity=user_to_create)
        return jsonify(access_token=access_token)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        
        if attempted_user and attempted_user.check_password_correction(
                attempted_password = form.password.data
        ):
            login_user(attempted_user)
            access_token = create_access_token(identity=attempted_user)
            return jsonify(access_token=access_token)
        else:
            return jsonify({"Unauthorized":"1"}), 401 

@app.route('/logout')
def logout_page():
    logout_user()
    return jsonify({
        "seccess":"true", 
        "message":"You are logged out" 
    }), 200 

# ML MODEL
# import numpy as np
# import pickle
# model = pickle.load(open('model.pkl', 'rb'))
# model = pickle.load(open('model.pkl', 'rb'))
# encoder = pickle.load(open('encoder.pkl', 'rb'))

# @app.route('/predict',methods=['POST'])
# def predict():
#     '''
#     For rendering results on HTML GUI
#     '''
#     int_features=[]
#     #int_features = [for x in request.form.values()]
#     for x in request.form.values():
#         int_features.append(x)
#         final_features = [np.array(int_features)]
#         char = encoder.fit_transform(final_features)
#         prediction = model.predict(char)

#     return jsonify({"prediction_text=":"the predicted price is :{}".format(prediction)})
import datetime
from Carweb import db , ma
from datetime import datetime

# intid = db.Integer()
db.metadata.clear()

class Annonce(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    likes_count = db.Column(db.Integer(), nullable=False )
    datePosted = db.Column(db.String() , default=datetime.utcnow)
    Car_id = db.Column(db.Integer(), db.ForeignKey("car.id"))
    owner_id = db.Column( db.Integer , db.ForeignKey("user.id"))
    
    def __init__(self, Car_id, owner_id):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.datePosted = current_time.__str__
        self.Car_id = Car_id
        self.owner_id= owner_id


class AnnonceSchema(ma.Schema):
    class Meta:
        feilds = (
            'id',
            'likes_count',
            'datePosted',
            'Car_id',
            'owner_id'
        )

class Car(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(length=80), nullable=False)
    name = db.Column(db.String(length=80), nullable=False)
    car_Brand = db.Column(db.String(length=80), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    fuel = db.Column(db.String(length=80), nullable=False)
    seats = db.Column(db.Integer(), nullable=False)
    region = db.Column(db.String(length=80), nullable=False)
    year = db.Column(db.Integer())
    kilos = db.Column(db.Integer(), nullable=False)
    desciption = db.Column(db.Text())
    
class CarsSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'title',
            'name',
            'car_Brand',
            'price',
            'fuel',
            'seats',
            'region',
            'year',
            'kilos',
            'desciption'
        )
car_schema= CarsSchema ()
cars_schema= CarsSchema(many=True)


    
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100))
    image = db.Column(db.Integer() , db.ForeignKey("userimage.id"))
    region = db.Column(db.String(length=80))
    phone_number = db.Column(db.String(10))
    
class UserSchema(ma.Schema):
    class Meta:
        feilds = (
            'id',
            'email',
            'password',
            'name',
            'image',
            'region',
            'phone_number'
        )



class Userimage(db.Model):
    id = db.Column(db.Integer() , primary_key = True)
    img = db.Column(db.LargeBinary)


class Annonceimage(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    img =  db.Column(db.LargeBinary)
    annonce_id = db.Column(db.Integer() , db.ForeignKey("annonce.id"))
    
class Avis(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    avi = db.Column(db.String(length=200), unique=False)
    sender_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer() , db.ForeignKey("user.id"))
    
class Comments(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String(length=200), unique=False)
    annonce_id = db.Column(db.Integer() , db.ForeignKey("annonce.id"))
    
class Annonce_favoris ( db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    annonce_id = db.Column(db.Integer() , db.ForeignKey("annonce.id"))
    user_id = db.Column( db.Integer() , db.ForeignKey("user.id"))
    

    
    

    

    
    
   
    
    
    
    
    
    
    
     

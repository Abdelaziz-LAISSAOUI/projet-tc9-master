from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '4b0c0a1a46a9468e69e54d9d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Carweb.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
# app.config['SECRET_KEY'] = '4b0c0a1a46a9468e69e54d9d'
db = SQLAlchemy(app)
if __name__ == '__main__':
    app.run(debug=True)
# from Carweb import routes
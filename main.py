from flask import Flask, app
from flask_restful import Api, Resource
from purchases.resources import purchases_v1
from returns.resources import returns_v1

app = Flask(__name__)
app.register_blueprint(purchases_v1)
app.register_blueprint(returns_v1)


if __name__ == "__main__":
  app.run(debug=True)
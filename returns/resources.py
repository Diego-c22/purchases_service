from flask import  Blueprint
from flask_restful import Api, Resource, abort, reqparse
import requests

# Common
from common.request import get_method, post_method

# Utilities
import datetime


returns_v1 = Blueprint('returns_v1', __name__)
api = Api(returns_v1)

class ReturnResource(Resource):
    def post(self):
        args = arguments.parse_args()

        request = get_method(f'tienda/compras/{args["id_compra"]}')
        if request.status_code == 404:
            abort(404, message='La compra no fue encontrada')
        
        res = request.json()
        request_validator = requests.post(f'192.168.191.16/validator/devolution.php/?claveDeRastreo={res["rastreocompras"]}')
        try:
          
          res_validator = request_validator.json()
        except:
            abort(request_validator.status_code, message="hubo un error al realizar la conexion")



        if res_validator['resultado'] == 'false':
            abort(400, message='Sucedio un error al realizar la devolución')

        response = post_method('tienda/devoluciones/', data = {
          'fechadevolucion': datetime.date.today(),
          'idarticulocomprado': args['id_articulo']
        })

        if response.status_code >= 400:
            res = response.json()
            abort(response.status_code, message=res)

        return response.json()


api.add_resource(ReturnResource, "/return/")

arguments = reqparse.RequestParser()
arguments.add_argument("id_compra", type=int, help="El id de compra es requerido", required=True)
arguments.add_argument("id_articulo", type=int, help="El id del articulo es requerido", required=True)
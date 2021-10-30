# Flask
from flask import  Blueprint
from flask_restful import Api, Resource, abort, reqparse
import requests

# Common
from common.request import get_method, post_method

# Utilities
import datetime

purchases_v1 = Blueprint('purchases_v1', __name__)
api = Api(purchases_v1)

class PurchaseResource(Resource):
    def get(self, id):
        response = get_method(f'tienda/compras/{id}')
        if len(response) == 0:
            abort(404, message="User doesn't have purchases")
        return response, 200
    

class PurchasesResource(Resource):
    
    def post(self):
        args = arguments.parse_args()

        request_item = get_method(f'tienda/articulos/{args["id_articulo"]}/')

        if request_item.status_code >= 400:
            res = request_item.json()
            abort(request_item.status_code, message=res)
        
        res = request_item.json()
        amount = float(res['precioventa']) * args['cantidad']
        
        """
        data = {
            "concepto": "Electronics",
            "monto": 5000,
            "numeroDeTarjetaDeudor": "1234567812678394",
            "cvvDeudor": "439",
            "fechaDeVencimientoDeudor": "2025-10",
            "numeroDeCuentaAcredor": "2"
        }
        """
        data = {
          'concepto': 'Electronics',
          'monto': amount,
          'numeroDeTarjetaDeudor': args['ntarjeta'],
          'cvvDeudor': args['cvv'],
          'fechaDeVencimientoDeudor': args['ftarjeta'],
          'numeroDeCuentaAcredor': '2'
        }
        
        request = requests.post('http://192.168.191.16/validador/action.php/', json=data)
        try:
            jrequest = request.json()
            print(jrequest)
        except: 
          abort(request.status_code, message="Sucedio un error al intentar conectarse")
        

        #request = {'resultado': True, 'claveDeRastreo': '12345'}

        if jrequest['resultado'] == 'false':
            abort(400, message="Sucedio un error al momento de realizar el pago. Vuelva a intentar")
          
        args['fechacompra'] = datetime.date.today()
        args['rastreocompras'] = jrequest['claveDeRastreo']

        request_purchase = post_method('tienda/compras/', data={
          'preciototal': amount,
          'fechacompra': datetime.date.today(),
          'rastreocompras': jrequest['claveDeRastreo'],
          'idusuario': args['id_usuario']
        })

        if request_purchase.status_code >= 400:
            abort(request_purchase.status_code, message=request_purchase.json())
        
        request_purchase = request_purchase.json()

        request_purchase = post_method('tienda/articulos_comprados/', data={
          'idcompra': request_purchase['idcompra'],
          'idarticulo': args['id_articulo'],
          'cantidad': args['cantidad']
        })

        if request_purchase.status_code > 300:
            abort(request_purchase.status_code, message=request_purchase.json())
        
        return {'message': 'La compra fue terminada con éxito'}, 200


api.add_resource(PurchaseResource, "/purchases/<int:id>")
api.add_resource(PurchasesResource, "/purchases/")

arguments = reqparse.RequestParser()
arguments.add_argument("ftarjeta", type=str, help="La fecha de vencimiento es obligatoria", required=True)
arguments.add_argument("cvv", type=int, help="El CVV es un cmapo obligatorio", required=True)
arguments.add_argument("ntarjeta", type=int, help="El numero de tarjeta es un campo obligatorio")
arguments.add_argument("id_articulo", type=int, help="El ID del articulo es un campo obligatorio", required=True)
arguments.add_argument("id_usuario", type=int, help="El ID de usuario es un campo obligatorio", required=True)
arguments.add_argument("cantidad", type=int, help="La cantidad de articulos es un campo obligatorio", required=True)
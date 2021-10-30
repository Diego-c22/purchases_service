import requests
data = {
            "concepto": "Electronics",
            "monto": 5000,
            "numeroDeTarjetaDeudor": "1234567812678394",
            "cvvDeudor": "439",
            "fechaDeVencimientoDeudor": "2025-10",
            "numeroDeCuentaAcredor": "2"
        }
request = requests.post('http://192.168.191.16/validador/action.php/', json=data)
print(request.text)
print(request.json())




# https://j2logo.com/flask/tutorial-como-crear-api-rest-python-con-flask/
# https://www.youtube.com/watch?v=GMppyAPbLYk
import requests
URL = 'http://127.0.0.1:8000/middleware/'

def get_method(url):
    try:
        response = requests.get(f'{URL}{url}')
    except:
        return {'message': 'Hubo un error en la conexion'}

    return response

def post_method(url, data):
    try:
        response = requests.post(f'{URL}{url}', data=data)
        response = response
    except:
        return {'message': 'Hubo un error en la conexion'}

    return response
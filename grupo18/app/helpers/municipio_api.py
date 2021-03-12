import requests

def get_municipio_by_id(id_municipio):
    return requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios/{0}'.format(id_municipio)).json()['data']['Town']

def get_municipios():
    totalMunicipios = requests.get(
        'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios').json()['total']
    payload = {'per_page': str(totalMunicipios)}
    return requests.get('https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios', params=payload).json()['data']['Town']
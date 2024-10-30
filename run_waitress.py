from waitress import serve
from docutrack.wsgi import application

if __name__ == '__main__':
    print("Servidor TRAMITEC iniciado...")
    serve(application, host='0.0.0.0', port=8000)

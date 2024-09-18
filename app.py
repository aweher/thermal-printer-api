#!/usr/bin/env python3
from flask import render_template
from printer_api import PrinterAPI

# Instanciar PrinterAPI
printer_api = PrinterAPI()

# Exponer el objeto Flask
app = printer_api.app

# Ruta para servir el frontend desde la carpeta 'templates'
@app.route('/')
def index():
    return render_template('index.html')  # Carga el archivo HTML desde la carpeta 'templates'

#!/usr/bin/env python3
from flask import render_template
from printer_api import PrinterAPI

# Instanciar PrinterAPI
printer_api = PrinterAPI()

# Exponer el objeto Flask
app = printer_api.app

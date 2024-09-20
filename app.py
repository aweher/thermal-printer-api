# -*- coding: utf-8 -*-
from printer_api import PrinterAPI

# Instanciar PrinterAPI
printer_api = PrinterAPI()

# Exponer el objeto Flask
app = printer_api.app

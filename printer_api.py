import os
import yaml
import base64
import requests
import logging
from flask import Flask, request, jsonify
from escpos.printer import Network, Usb
from io import BytesIO
from PIL import Image

# Tamaño máximo en píxeles para un rollo de 80mm (por ejemplo, 576 píxeles de ancho)
MAX_IMAGE_WIDTH = 576

class EpsonPrinter:
    def __init__(self, config_file='config.yaml'):
        # Configurar logging
        self.logger = logging.getLogger('EpsonPrinter')
        handler = logging.FileHandler('logs/epson_printer.log')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        # Verificar si config_file es un diccionario o una cadena (ruta del archivo)
        if isinstance(config_file, dict):
            self.config = config_file  
        else:
            self.config = self.load_config(config_file)
        self.printer = None

    def load_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
            raise FileNotFoundError(f"Could not load config file: {e}")

    def connect(self):
        try:
            printer_type = self.config['printer']['type']
            if printer_type == "network":
                ip_address = self.config['printer']['network']['ip_address']
                port = self.config['printer']['network']['port']
                self.printer = Network(ip_address, port)
                self.logger.info(f"Connected to network printer at {ip_address}:{port}")
            elif printer_type == "usb":
                id_vendor = self.config['printer']['usb']['idVendor']
                id_product = self.config['printer']['usb']['idProduct']
                self.printer = Usb(id_vendor, id_product)
                self.logger.info(f"Connected to USB printer with Vendor ID: {id_vendor}, Product ID: {id_product}")
            else:
                raise ValueError("Unsupported printer type in configuration.")
        except Exception as e:
            self.logger.error(f"Error connecting to printer: {e}")
            raise ConnectionError(f"Connection error: {e}")

    def disconnect(self):
        try:
            if self.printer is not None:
                self.printer.close()
                self.logger.info("Printer connection closed.")
            else:
                self.logger.warning("Attempted to close printer connection, but printer is not connected.")
        except Exception as e:
            self.logger.error(f"Error disconnecting from printer: {e}")

    def resize_image_for_printer(self, image):
        """Resize the image to fit the printer's width, if necessary."""
        width, height = image.size

        # Si el ancho de la imagen es mayor que el tamaño máximo permitido, redimensionar
        if width > MAX_IMAGE_WIDTH:
            new_height = int((MAX_IMAGE_WIDTH / width) * height)
            image = image.resize((MAX_IMAGE_WIDTH, new_height), Image.LANCZOS)  # Usar Image.LANCZOS directamente
            print(f"Image resized to {MAX_IMAGE_WIDTH}px width and {new_height}px height")

        return image
    
    def print_text(self, text):
        try:
            if self.printer is None:
                self.connect()
            
            self.printer.text(text)
            self.printer.cut()
            self.logger.info(f"Text printed: {text}")
            return True
        except Exception as e:
            self.logger.error(f"Error printing text: {e}")
            return False
        finally:
            self.disconnect()

    def print_qr(self, data):
        try:
            if self.printer is None:
                self.connect()

            self.printer.qr(data)
            self.printer.cut()
            self.logger.info(f"QR code printed: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error printing QR code: {e}")
            return False
        finally:
            self.disconnect()

    def print_barcode(self, data):
        try:
            if self.printer is None:
                self.connect()

            self.printer.barcode(data, "EAN13", 64, 2, '', '')
            self.printer.cut()
            self.logger.info(f"Barcode printed: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error printing barcode: {e}")
            return False
        finally:
            self.disconnect()

    def print_image(self, image_data):
        try:
            if self.printer is None:
                self.connect()

            image = Image.open(BytesIO(base64.b64decode(image_data)))

            image = self.resize_image(image)

            self.printer.image(image)
            self.printer.cut()
            self.logger.info("Image printed.")
            return True
        except Exception as e:
            self.logger.error(f"Error printing image: {e}")
            return False
        finally:
            self.disconnect()
    
    def resize_image(self, image):
        try:
            width_percent = (MAX_IMAGE_WIDTH / float(image.size[0]))
            height_size = int((float(image.size[1]) * float(width_percent)))
            resized_image = image.resize((MAX_IMAGE_WIDTH, height_size), Image.Resampling.LANCZOS)
            return resized_image
        except Exception as e:
            self.logger.error(f"Error resizing image: {e}")
            raise RuntimeError(f"Failed to resize image: {e}")

    def print_image_from_url(self, image_url):
        try:
            if self.printer is None:
                self.connect()

            response = requests.get(image_url)
            if response.status_code != 200:
                self.logger.error(f"Failed to download image from URL: {image_url}")
                return False

            image = Image.open(BytesIO(response.content))

            image = self.resize_image(image)

            self.printer.image(image)
            self.printer.cut()
            self.logger.info(f"Image printed from URL: {image_url}")
            return True
        except Exception as e:
            self.logger.error(f"Error printing image from URL: {e}")
            return False
        finally:
            self.disconnect()

class PrinterAPI:
    def __init__(self, config_file='config.yaml'):
        self.app = Flask(__name__)
        self.config = self.load_config(config_file)
        self.printer = EpsonPrinter(self.config)
        self.setup_routes()

    def load_config(self, config_file):
        """
        Load configuration from YAML file and environment variables.
        """
        config = {}

        # Load the configuration from YAML file
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)

        # Override with environment variables if they exist
        config['printer_type'] = os.getenv('PRINTER_TYPE', config.get('printer', {}).get('type', 'network'))
        config['network_ip'] = os.getenv('NETWORK_IP', config.get('printer', {}).get('network', {}).get('ip_address', 'localhost'))
        config['network_port'] = os.getenv('NETWORK_PORT', config.get('printer', {}).get('network', {}).get('port', 9100))
        config['usb_vendor'] = os.getenv('USB_VENDOR', config.get('printer', {}).get('usb', {}).get('idVendor', 0x04b8))
        config['usb_product'] = os.getenv('USB_PRODUCT', config.get('printer', {}).get('usb', {}).get('idProduct', 0x0e15))

        return config

    def setup_routes(self):
        @self.app.route('/status')
        def home():
            return f"Epson TM-m30ii API - Printer type: {self.config['printer_type']}"

        # Print text
        @self.app.route('/print', methods=['POST'])
        def print_message():
            try:
                data = request.json
                message = data.get('message')

                if not message:
                    return jsonify({"status": "error", "message": "'message' field is required"}), 400
                
                if self.printer.print_text(message):
                    return jsonify({"status": "success", "message": "Text printed successfully"})
                else:
                    return jsonify({"status": "error", "message": "Failed to print text"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

        # Print QR code
        @self.app.route('/print/qr', methods=['POST'])
        def print_qr():
            try:
                data = request.json
                qr_data = data.get('data')

                if not qr_data:
                    return jsonify({"status": "error", "message": "'data' field is required for QR"}), 400
                
                if self.printer.print_qr(qr_data):
                    return jsonify({"status": "success", "message": "QR code printed successfully"})
                else:
                    return jsonify({"status": "error", "message": "Failed to print QR code"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

        # Print barcode
        @self.app.route('/print/barcode', methods=['POST'])
        def print_barcode():
            try:
                data = request.json
                barcode_data = data.get('data')

                if not barcode_data:
                    return jsonify({"status": "error", "message": "'data' field is required for barcode"}), 400
                
                if self.printer.print_barcode(barcode_data):
                    return jsonify({"status": "success", "message": "Barcode printed successfully"})
                else:
                    return jsonify({"status": "error", "message": "Failed to print barcode"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

        # Print image (base64)
        @self.app.route('/print/image', methods=['POST'])
        def print_image():
            try:
                data = request.json
                image_data = data.get('image_data')

                if not image_data:
                    return jsonify({"status": "error", "message": "'image_data' field is required for image"}), 400

                try:
                    base64.b64decode(image_data)
                except Exception:
                    return jsonify({"status": "error", "message": "Invalid base64-encoded image"}), 400

                if self.printer.print_image(image_data):
                    return jsonify({"status": "success", "message": "Image printed successfully"})
                else:
                    return jsonify({"status": "error", "message": "Failed to print image"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

        # Print image from URL
        @self.app.route('/print/image-url', methods=['POST'])
        def print_image_url():
            try:
                data = request.json
                image_url = data.get('image_url')

                if not image_url:
                    return jsonify({"status": "error", "message": "'image_url' field is required"}), 400

                if self.printer.print_image_from_url(image_url):
                    return jsonify({"status": "success", "message": "Image printed successfully from URL"})
                else:
                    return jsonify({"status": "error", "message": "Failed to print image from URL"})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(debug=True, host=host, port=port)

if __name__ == '__main__':
    # Start the API with the YAML config file
    printer_api = PrinterAPI(config_file='config.yaml')
    printer_api.run()
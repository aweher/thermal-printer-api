
# Epson TM-m30ii API

This is a Flask-based API for controlling an **Epson TM-m30ii thermal printer** using the **python-escpos** library. The API supports printing text, QR codes, barcodes, base64-encoded images, and images from URLs.

## Features

- Print plain text
- Print QR codes
- Print barcodes (EAN13 format)
- Print base64-encoded images
- Print images from URLs
- Automatic image resizing for 80mm thermal paper rolls (576 pixels width)

## Prerequisites

- **Python 3.7+**
- Epson TM-m30ii or similar thermal printer
- Network or USB connection to the printer

### Required Python packages

Install the required dependencies using `pip3`:

```bash
pip install -r requirements.txt
```

## Configuration

The printer is configured via a **YAML** file (`config.yaml`). This file allows you to specify whether the printer is connected via **network** or **USB**.

### Example `config.yaml`

```yaml
printer:
  type: network  # Can be "network" or "usb"
  network:
    ip_address: "192.168.X.Y"
    port: 9100
  usb:
    idVendor: 0x04b8  # Epson
    idProduct: 0x0e2a  # TM-M30II
```

## Running the API

1. Make sure your printer is connected (either via network or USB).
2. Configure your `config.yaml` file.
3. Run the Flask app:

```bash
python app.py
```

The API will run on `http://localhost:5000` by default.

## API Endpoints

### 1. **Print Text**

Print plain text to the printer.

- **URL**: `/print`
- **Method**: `POST`
- **Body**:
  
  ```json
  {
    "message": "Hello, World!"
  }
  ```

Example cURL:

```bash
curl -X POST http://localhost:5000/print -H "Content-Type: application/json" -d '{"message": "Hello, World!"}'
```

### 2. **Print QR Code**

Print a QR code with the provided data.

- **URL**: `/print/qr`
- **Method**: `POST`
- **Body**:

  ```json
  {
    "data": "https://example.com"
  }
  ```

Example cURL:

```bash
curl -X POST http://localhost:5000/print/qr -H "Content-Type: application/json" -d '{"data": "https://example.com"}'
```

### 3. **Print Barcode**

Print a barcode (EAN13 format) with the provided data.

- **URL**: `/print/barcode`
- **Method**: `POST`
- **Body**:

  ```json
  {
    "data": "123456789012"
  }
  ```

Example cURL:

```bash
curl -X POST http://localhost:5000/print/barcode -H "Content-Type: application/json" -d '{"data": "123456789012"}'
```

### 4. **Print Base64-Encoded Image**

Print an image from base64-encoded data. The image is resized automatically to fit 80mm thermal paper (576 pixels width).

- **URL**: `/print/image`
- **Method**: `POST`
- **Body**:

  ```json
  {
    "image_data": "base64encodedimagestring"
  }
  ```

Example cURL:

```bash
curl -X POST http://localhost:5000/print/image -H "Content-Type: application/json" -d '{"image_data": "iVBORw0KGgoAAAANSUhEUgAA..."}'
```

### 5. **Print Image from URL**

Print an image directly from a URL. The image will be resized automatically to fit 80mm thermal paper (576 pixels width).

- **URL**: `/print/image-url`
- **Method**: `POST`
- **Body**:

  ```json
  {
    "image_url": "https://example.com/image.png"
  }
  ```

Example cURL:

```bash
curl -X POST http://localhost:5000/print/image-url -H "Content-Type: application/json" -d '{"image_url": "https://example.com/image.png"}'
```

## Image Resizing

For all image endpoints, the API automatically resizes the image to fit an 80mm thermal paper roll. The maximum width is **576 pixels**. If the image exceeds this width, it will be resized while maintaining its aspect ratio.

## Error Handling

- If any required fields are missing, the API will return a `400 Bad Request` response with an error message.
- If an image URL is invalid or the image cannot be downloaded, the API will return a `400 Bad Request` response.

## License

This project is licensed under the MIT License.

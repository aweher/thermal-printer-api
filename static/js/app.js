// Función para imprimir texto
function printText() {
    const text = document.getElementById('print-text').value;
    fetch('/print', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: text }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Text printing result: ${data.message}`;
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error}`;
    });
}

// Función para imprimir un código QR
function printQR() {
    const qrData = document.getElementById('qr-data').value;
    fetch('/print/qr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: qrData }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `QR code printing result: ${data.message}`;
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error}`;
    });
}

// Función para imprimir una imagen desde URL
function printImage() {
    const imageUrl = document.getElementById('image-url').value;
    fetch('/print/image-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_url: imageUrl }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Image printing result: ${data.message}`;
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error}`;
    });
}

// Función para imprimir código de barras
function printBarcode() {
    const barcodeData = document.getElementById('barcode-data').value;
    fetch('/print/barcode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: barcodeData }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Barcode printing result: ${data.message}`;
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error}`;
    });
}
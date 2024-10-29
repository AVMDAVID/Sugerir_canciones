import requests

# URL de la API de Google Sheets (URL generada en el paso 3)
url = "https://script.google.com/macros/s/AKfycbwdGB0Nc_TMoUDKTOVAIUvqsyH5_npKDGs-t291dmn1SXotZMp2vecT-P-ar6HtLzaY/exec"

# Información de la sugerencia
sugerencia = {
    "nombre_cancion": "Nombre de la canción aquí",
    "artista": "Nombre del artista aquí"
}

# Enviar la solicitud a Google Sheets
response = requests.post(url, json=sugerencia)

if response.status_code == 200:
    print("Sugerencia enviada correctamente a Google Sheets.")
else:
    print("Error al enviar la sugerencia.")

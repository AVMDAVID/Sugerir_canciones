from flask import Flask, render_template, request, redirect, flash
from google.oauth2 import service_account
import gspread
import json  # Importa json para convertir el contenido del secreto en un objeto
from datetime import datetime
import os  # Importa el módulo os para acceder a las variables de entorno

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Necesario para flash messages

# Obtén el contenido del secreto desde la variable de entorno
cred_file_content = os.environ.get('GOOGLE_SHEET_CREDENTIALS')  # Usa el nombre exacto de tu variable de entorno

# Verifica que la variable de entorno esté configurada
if not cred_file_content:
    raise ValueError("La variable de entorno 'GOOGLE_SHEET_CREDENTIALS' no está configurada correctamente.")

# Carga las credenciales desde el contenido del secreto (JSON)
creds = service_account.Credentials.from_service_account_info(
    json.loads(cred_file_content),
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

client = gspread.authorize(creds)
spreadsheet_id = "1NrgGLDDv5oZV9qSfRP4LrrVo039zJMPP7ahRf2g7L6k"
spreadsheet = client.open_by_key(spreadsheet_id)
worksheet = spreadsheet.sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    cancion = request.form['cancion'].strip().upper()
    artista = request.form['artista'].strip().upper()
    fecha_sugerencia = datetime.now().strftime('%d-%m-%Y')

    # Check for duplicates
    existing_records = worksheet.get_all_records()
    for record in existing_records:
        if record.get('Nombre de la Canción', '').upper() == cancion and record.get('Artista', '').upper() == artista:
            flash('Esta canción ya ha sido registrada. Por favor, ingrese una diferente.')
            return redirect('/')

    worksheet.append_row([cancion, artista, "📩 Enviada", fecha_sugerencia])
    flash('Canción registrada exitosamente.')
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obtiene el puerto de Render o usa 5000 localmente
    app.run(debug=True, host='0.0.0.0', port=port)

from flask import Flask, render_template, request, redirect
from google.oauth2 import service_account
import gspread
from datetime import datetime

app = Flask(__name__)

creds = service_account.Credentials.from_service_account_file('sugerencias-de-canciones-794434182960.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets"]  # Asegúrate de incluir el scope correcto
)

# Autenticación con Google Sheets
client = gspread.authorize(creds)

# Abre la hoja de cálculo
spreadsheet_id = "1NrgGLDDv5oZV9qSfRP4LrrVo039zJMPP7ahRf2g7L6k"  # Reemplaza esto con tu ID
spreadsheet = client.open_by_key(spreadsheet_id)
worksheet = spreadsheet.sheet1  # Selecciona la primera hoja

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    cancion = request.form['cancion'].upper()
    artista = request.form['artista'].upper()
    fecha_sugerencia = datetime.now().strftime('%d-%m-%Y')  # Captura la fecha actual en formato DD-MM-AAAA
    
    # Agregar datos a la hoja de cálculo
    worksheet.append_row([cancion, artista, "📩 Enviada", fecha_sugerencia])

    return redirect('/')  # Redirige de vuelta al formulario

if __name__ == '__main__':
    app.run(debug=True)

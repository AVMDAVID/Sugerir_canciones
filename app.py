from flask import Flask, render_template, request, redirect
from google.oauth2 import service_account
import gspread
from datetime import datetime
import os  # Importa el módulo os para obtener el puerto de Heroku

app = Flask(__name__)

creds = service_account.Credentials.from_service_account_file(
    'sugerencias-de-canciones-794434182960.json',
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
    cancion = request.form['cancion'].upper()
    artista = request.form['artista'].upper()
    fecha_sugerencia = datetime.now().strftime('%d-%m-%Y')
    worksheet.append_row([cancion, artista, "📩 Enviada", fecha_sugerencia])
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obtiene el puerto de Heroku o usa 5000 localmente
    app.run(debug=True, host='0.0.0.0', port=port)

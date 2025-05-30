from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Autenticación con Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # este archivo debe estar en tu proyecto
SPREADSHEET_NAME = "TareasMama"

def conectar_hoja():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    return sheet

def leer_tareas_pendientes():
    sheet = conectar_hoja()
    tareas = sheet.get_all_records()
    return [t for t in tareas if t.get("estado", "").lower() == "pendiente"]

def agregar_tarea(fecha, asunto, responsable):
    sheet = conectar_hoja()
    sheet.append_row([fecha, asunto, responsable, "pendiente"])

def marcar_como_terminada(indice):
    sheet = conectar_hoja()
    tareas = sheet.get_all_records()
    if 0 <= indice < len(tareas):
        # +2 por el encabezado y 1-indexing de Google Sheets
        row_number = indice + 2
        sheet.update_cell(row_number, 4, "terminada")  # columna 4 = estado

@app.route('/')
def index():
    tareas = leer_tareas_pendientes()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    fecha = request.form['fecha']
    asunto = request.form['asunto']
    responsable = request.form['responsable']
    agregar_tarea(fecha, asunto, responsable)
    return redirect('/')

@app.route('/completar/<int:indice>')
def completar(indice):
    marcar_como_terminada(indice)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

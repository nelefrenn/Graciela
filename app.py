from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
CSV_FILE = 'tareas.csv'
FIELDNAMES = ['fecha', 'asunto', 'responsable', 'estado']

def asegurar_csv_existe():
    """Crea el archivo CSV con encabezado si no existe"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def leer_tareas():
    asegurar_csv_existe()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        tareas = list(csv.DictReader(f))
        return [t for t in tareas if t['estado'] == 'pendiente']

def escribir_tarea(fecha, asunto, responsable):
    nueva_tarea = {
        'fecha': fecha,
        'asunto': asunto,
        'responsable': responsable,
        'estado': 'pendiente'
    }
    print("Registrando tarea:", nueva_tarea)  # depuración
    asegurar_csv_existe()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(nueva_tarea)

def marcar_como_terminada(indice):
    asegurar_csv_existe()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        tareas = list(csv.DictReader(f))

    if 0 <= indice < len(tareas):
        tareas[indice]['estado'] = 'terminada'

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(tareas)

@app.route('/')
def index():
    tareas = leer_tareas()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    fecha = request.form['fecha']
    asunto = request.form['asunto']
    responsable = request.form['responsable']
    escribir_tarea(fecha, asunto, responsable)
    return redirect('/')

@app.route('/completar/<int:indice>')
def completar(indice):
    marcar_como_terminada(indice)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



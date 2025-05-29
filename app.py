 app.py
from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'tareas.csv'

def leer_tareas():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def escribir_tarea(fecha, asunto, responsable):
    nueva_tarea = {'fecha': fecha, 'asunto': asunto, 'responsable': responsable}
    existe = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['fecha', 'asunto', 'responsable'])
        if not existe:
            writer.writeheader()
        writer.writerow(nueva_tarea)

def borrar_tarea(indice):
    tareas = leer_tareas()
    if 0 <= indice < len(tareas):
        tareas.pop(indice)
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['fecha', 'asunto', 'responsable'])
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
    borrar_tarea(indice)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'database.db'

def conectar_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla_si_no_existe():
    with conectar_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                asunto TEXT NOT NULL,
                responsable TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'pendiente'
            )
        ''')
        conn.commit()

def obtener_tareas_pendientes():
    with conectar_db() as conn:
        tareas = conn.execute("SELECT * FROM tareas WHERE estado = 'pendiente'").fetchall()
    return tareas

def agregar_tarea(fecha, asunto, responsable):
    with conectar_db() as conn:
        conn.execute('''
            INSERT INTO tareas (fecha, asunto, responsable, estado)
            VALUES (?, ?, ?, 'pendiente')
        ''', (fecha, asunto, responsable))
        conn.commit()

def marcar_como_terminada(id_tarea):
    with conectar_db() as conn:
        conn.execute("UPDATE tareas SET estado = 'terminada' WHERE id = ?", (id_tarea,))
        conn.commit()

@app.route('/')
def index():
    crear_tabla_si_no_existe()
    tareas = obtener_tareas_pendientes()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar', methods=['POST'])
def agregar():
    fecha = request.form['fecha']
    asunto = request.form['asunto']
    responsable = request.form['responsable']
    agregar_tarea(fecha, asunto, responsable)
    return redirect('/')

@app.route('/completar/<int:id_tarea>')
def completar(id_tarea):
    marcar_como_terminada(id_tarea)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



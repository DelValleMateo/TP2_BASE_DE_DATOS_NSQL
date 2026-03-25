from flask import Flask, render_template, request, redirect, url_for, flash
import redis

app = Flask(__name__)
app.secret_key = 'mandalorian_secret_key_123'

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_capitulos_info():
    """Retorna la información estática de los 24 capítulos."""
    return [
        {"id": 1, "titulo": "Capítulo 1: El mandaloriano (The Mandalorian)", "precio": 500},
        {"id": 2, "titulo": "Capítulo 2: El niño (The Child)", "precio": 500},
        {"id": 3, "titulo": "Capítulo 3: El pecado (The Sin)", "precio": 500},
        {"id": 4, "titulo": "Capítulo 4: Santuario (Sanctuary)", "precio": 500},
        {"id": 5, "titulo": "Capítulo 5: El pistolero (The Gunslinger)", "precio": 500},
        {"id": 6, "titulo": "Capítulo 6: El prisionero (The Prisoner)", "precio": 500},
        {"id": 7, "titulo": "Capítulo 7: El ajuste de cuentas (The Reckoning)", "precio": 500},
        {"id": 8, "titulo": "Capítulo 8: Redención (Redemption)", "precio": 500},
        {"id": 9, "titulo": "Capítulo 9: El mariscal (The Marshal)", "precio": 500},
        {"id": 10, "titulo": "Capítulo 10: La pasajera (The Passenger)", "precio": 500},
        {"id": 11, "titulo": "Capítulo 11: La heredera (The Heiress)", "precio": 500},
        {"id": 12, "titulo": "Capítulo 12: El asedio (The Siege)", "precio": 500},
        {"id": 13, "titulo": "Capítulo 13: La Jedi (The Jedi)", "precio": 500},
        {"id": 14, "titulo": "Capítulo 14: La tragedia (The Tragedy)", "precio": 500},
        {"id": 15, "titulo": "Capítulo 15: El creyente (The Believer)", "precio": 500},
        {"id": 16, "titulo": "Capítulo 16: El rescate (The Rescue)", "precio": 500},
        {"id": 17, "titulo": "Capítulo 17: El apóstata (The Apostate)", "precio": 500},
        {"id": 18, "titulo": "Capítulo 18: Las minas de Mandalore (The Mines of Mandalore)", "precio": 500},
        {"id": 19, "titulo": "Capítulo 19: El converso (The Convert)", "precio": 500},
        {"id": 20, "titulo": "Capítulo 20: El huérfano (The Foundling)", "precio": 500},
        {"id": 21, "titulo": "Capítulo 21: El pirata (The Pirate)", "precio": 500},
        {"id": 22, "titulo": "Capítulo 22: Pistoleros a sueldo (Guns for Hire)", "precio": 500},
        {"id": 23, "titulo": "Capítulo 23: Los espías (The Spies)", "precio": 500},
        {"id": 24, "titulo": "Capítulo 24: El regreso (The Return)", "precio": 500},
    ]

def obtener_estado_capitulo(id_capitulo):
    """
    Consulta en Redis el estado de un capítulo.
    Si la clave no existe o expiró, retorna 'Disponible'.
    """
    estado = r.get(f"mandalorian:capitulo:{id_capitulo}")
    if not estado:
        return "Disponible"
    return estado

@app.route('/')
def index():
    capitulos = get_capitulos_info()
    for cap in capitulos:
        # Añadimos el estado actual consultado desde Redis
        cap['estado'] = obtener_estado_capitulo(cap['id'])
        
    return render_template('index.html', capitulos=capitulos)

@app.route('/reservar/<int:id_capitulo>', methods=['POST'])
def reservar(id_capitulo):
    estado_actual = obtener_estado_capitulo(id_capitulo)
    if estado_actual == "Disponible":
        # Guardar en Redis como 'Reservado' con TTL de 240 segundos (4 minutos)
        r.setex(f"mandalorian:capitulo:{id_capitulo}", 240, "Reservado")
        flash(f'Capítulo {id_capitulo} reservado exitosamente. Tienes 4 minutos para pagar.', 'success')
    else:
        flash(f'El capítulo {id_capitulo} no se encuentra disponible para reserva.', 'error')
    
    return redirect(url_for('index'))

@app.route('/alquilar/<int:id_capitulo>', methods=['POST'])
def alquilar(id_capitulo):
    estado_actual = obtener_estado_capitulo(id_capitulo)
    precio = request.form.get('precio', '0')
    
    # Se puede concretar el alquiler si está Disponible o Reservado
    if estado_actual in ["Disponible", "Reservado"]:
        # Guardar en Redis como 'Alquilado' con TTL de 86400 segundos (24 horas)
        r.setex(f"mandalorian:capitulo:{id_capitulo}", 86400, "Alquilado")
        flash(f'¡Capítulo {id_capitulo} alquilado exitosamente por 24 horas! (Monto pagado: ${precio})', 'success')
    else:
        flash(f'El capítulo {id_capitulo} ya se encuentra alquilado.', 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Habilitar debug y correr en el puerto 5000 por defecto
    app.run(debug=True, port=5000)

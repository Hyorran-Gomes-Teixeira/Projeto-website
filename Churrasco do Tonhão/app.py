from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Configurações do banco de dados
db_config = {
    "host": "localhost",
    "user": "seu_usuario",
    "password": "sua_senha",
    "database": "churrasco_do_tonhao"
}

# Função para conexão com o banco de dados
def db_connection():
    db = mysql.connector.connect(**db_config)
    return db

# Rotas da API 1
@app.route('/reservas', methods=['GET'])
def obter_reservas():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, telefone, lugares, data, horario, status FROM reservas")
        reservas = cursor.fetchall()
        return jsonify(reservas)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/atualizar_reserva', methods=['GET'])
def atualizar_reserva():
    conn = None
    cursor = None
    try:
        reserva_id = request.args.get('id')
        novo_status = request.args.get('status')
        print(f"Parâmetros recebidos - ID: {reserva_id}, Status: {novo_status}")
        if not reserva_id or not novo_status:
            return jsonify({"error": "ID ou status não fornecidos"}), 400
        if not reserva_id.isdigit():
            return jsonify({"error": "ID inválido."}), 400
        reserva_id = int(reserva_id)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET status = %s WHERE id = %s", (novo_status, reserva_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Reserva não encontrada."}), 404
        return jsonify({"success": True})
    except ValueError as ve:
        print(f"Erro de ValueError: {ve}")
        return jsonify({"error": "ID inválido."}), 400
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/excluir_reserva', methods=['DELETE'])
def excluir_reserva():
    try:
        reserva_id = request.args.get('id')
        if not reserva_id or not reserva_id.isdigit():
            return jsonify({"error": "ID inválido."}), 400
        reserva_id = int(reserva_id)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Reserva não encontrada."}), 404
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

# Rotas da API 2
@app.route('/reservar', methods=['POST'])
def reservar():
    data = request.json
    nome = data['nome']
    telefone = data['telefone']
    lugares = data['lugares']
    data_reserva = data['data']
    horario = data['horario']
    db = db_connection()
    cursor = db.cursor()
    sql = "INSERT INTO reservas (nome, telefone, lugares, data, horario) VALUES (%s, %s, %s, %s, %s)"
    valores = (nome, telefone, lugares, data_reserva, horario)
    cursor.execute(sql, valores)
    db.commit()
    cursor.close()
    db.close()
    return '', 204

@app.route('/reservas', methods=['GET'])
def get_reservas():
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(reservas)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify,request
from servicio import UsuarioServicio

app = Flask(__name__)
servicio = UsuarioServicio()

@app.route('/api/usuarios/registro', methods=['POST'])
def registrar_usuario():
    datos_json = request.get_json()
    if not datos_json:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    respuesta,codigo_http = servicio.registrar_usuario(datos_json)
    return jsonify(respuesta), codigo_http

@app.route('/api/usuarios/login', methods=['POST'])
def login_usuario():
    try:
        datos_json = request.get_json()
        if not datos_json:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        correo = datos_json.get("correo")
        password = datos_json.get("password")

        if not correo or not password:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        respuesta,codigo_http = servicio.login_usuario(correo, password)
        return jsonify(respuesta), codigo_http
    
    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True,port=5000)


# $2b$12$p4esNsagHIAT9uv7f335GekTf4WeFrzOFj/g7CWlrT4TC7nDCdS.C

# $2b$ -> version de Bcrypt
# 12 -> costo
# p4esNsagHIAT9uv -> salt
# g7CWlrT4TC7nDCdS.C -> hash

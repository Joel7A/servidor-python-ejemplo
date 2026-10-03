import bcrypt
from repositorio import UsuarioRepositorio
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ServicioSeguridad")

class UsuarioServicio:
    def __init__(self):
        self.repositorio = UsuarioRepositorio()

    def registrar_usuario(self, datos):

        nombre = datos.get("nombre")
        correo = datos.get("correo")
        password = datos.get("password")

        if not nombre or not correo or not password:
            return {"error": "Faltan datos requeridos"}, 400

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        resultado = self.repositorio.registrar_usuario(nombre, correo, password_hash)

        if resultado:
            return {"mensaje": "Usuario registrado exitosamente"}, 201
        else:
            return {"error": "Error al registrar el usuario"}, 500

    def login_usuario(self, correo, password):
        if not correo or not password:
            return {"error": "Faltan datos requeridos"}, 400

        usuario = self.repositorio.obtener_usuario_por_correo(correo)
        logger.info(f"Usuario encontrado en BD (ID: {usuario['id']}). Extrayendo hash guardado...")
        hash_almacenado = usuario['password_hash']
        logger.info(f"Hash recuperado de MySQL: {hash_almacenado[:30]}...")

        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        ##verifica la contraseña ingresada con la contraseña almacenada en la base de datos
        logger.info("Comparando contraseña plana ingresada contra el hash almacenado usando Bcrypt...")
        password_valida = bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8'))
        logger.info(f"Resultado de la verificación: {password_valida}")

        if password_valida:
            return {"mensaje": "Inicio de sesión exitoso"}, 200
        else:
            return {"error": "Contraseña incorrecta"}, 401
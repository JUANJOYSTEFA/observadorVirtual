from passlib.hash import pbkdf2_sha256
from Modulos.Observador.models import Estudiante, Acudiente, Administrativos
import logging

# Configurar el logger (si no usas el de Django)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='migracion_contrasenas.log'
)
logger = logging.getLogger(__name__)

def migrarContrasenasPlanas():
    """
    Script para migrar contraseñas en texto plano a formato hasheado
    """
    print("Iniciando migración de contraseñas...")
    
    # Lista de modelos que tienen campo de contraseña
    modelos = [Estudiante, Acudiente, Administrativos]
    contadorTotal = 0
    
    for modelo in modelos:
        print(f"Procesando modelo: {modelo.__name__}")
        logger.info(f"Iniciando migración de contraseñas para modelo: {modelo.__name__}")
        
        # Obtener todos los usuarios del modelo actual
        usuarios = modelo.objects.all()
        contadorModelo = 0
        
        for usuario in usuarios:
            # Verificar si la contraseña ya es un hash
            if not usuario.contrasena.startswith('$pbkdf2'):
                try:
                    # Guardar la contraseña original
                    contrasenaOriginal = usuario.contrasena
                    
                    # Crear hash de la contraseña
                    contrasenaHash = pbkdf2_sha256.hash(contrasenaOriginal)
                    
                    # Actualizar la contraseña en la base de datos
                    usuario.contrasena = contrasenaHash
                    usuario.save()
                    
                    contadorModelo += 1
                    logger.info(f"Contraseña migrada exitosamente para: {usuario.correo}")
                    print(f"✓ Migrada: {usuario.correo}")
                except Exception as e:
                    logger.error(f"Error al migrar contraseña para {usuario.correo}: {str(e)}")
                    print(f"✗ Error al migrar: {usuario.correo} - {str(e)}")
            else:
                print(f"⚠ Ya hasheada (omitida): {usuario.correo}")
        
        contadorTotal += contadorModelo
        print(f"Migración completada para {modelo.__name__}: {contadorModelo} contraseñas actualizadas")
    
    print(f"Proceso finalizado. Total de contraseñas migradas: {contadorTotal}")
    logger.info(f"Migración completa. Total: {contadorTotal} contraseñas")
    return contadorTotal

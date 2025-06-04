from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Se importa la cadena de conexión desde configuracion.py
from configuracion import cadena_base_datos

# Crear el motor de la base de datos
engine = create_engine(cadena_base_datos)

# Declarativa base
Base = declarative_base()

# Clase Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    publicaciones = relationship("Publicacion", back_populates="usuario")
    reacciones = relationship("Reaccion", back_populates="usuario")

    def __repr__(self):
        return f"Usuario: nombre={self.nombre}"

# Clase Publicacion
class Publicacion(Base):
    __tablename__ = 'publicaciones'
    id = Column(Integer, primary_key=True)
    contenido = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("Reaccion", back_populates="publicacion")

    def __repr__(self):
        return f"Publicacion: {self.contenido[:30]}..."

# Clase Reaccion
class Reaccion(Base):
    __tablename__ = 'reacciones'
    id = Column(Integer, primary_key=True)
    tipo_emocion = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id'))

    usuario = relationship("Usuario", back_populates="reacciones")
    publicacion = relationship("Publicacion", back_populates="reacciones")

    __table_args__ = (UniqueConstraint('usuario_id', 'publicacion_id', name='uix_usuario_publicacion'),)

    def __repr__(self):
        return f"Reaccion: {self.tipo_emocion} - UsuarioID={self.usuario_id} - PublicacionID={self.publicacion_id}"

# Crear todas las tablas en la base
Base.metadata.create_all(engine)

# Crear la sesión para operaciones posteriores
Session = sessionmaker(bind=engine)
session = Session()

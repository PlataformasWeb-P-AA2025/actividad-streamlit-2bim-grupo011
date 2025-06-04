import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from genera_tablas import Usuario, Publicacion, Reaccion
from configuracion import cadena_base_datos

# Leer los CSVs
usuarios_df = pd.read_csv("DATA/usuarios_red_x.csv")
publicaciones_df = pd.read_csv("DATA/usuarios_publicaciones.csv", delimiter="|", names=["usuario", "publicacion"])
emociones_df = pd.read_csv("DATA/usuario_publicacion_emocion.csv", delimiter="|", names=["usuario", "comentario", "tipo_emocion"])

# Conectar a la base de datos
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# Insertar usuarios
for nombre in usuarios_df['usuario'].unique():
    if not session.query(Usuario).filter_by(nombre=nombre).first():
        session.add(Usuario(nombre=nombre))
session.commit()

# Insertar publicaciones
for index, row in publicaciones_df.iterrows():
    usuario = session.query(Usuario).filter_by(nombre=row['usuario']).first()
    if usuario:
        existe = session.query(Publicacion).filter_by(contenido=row['publicacion'], usuario_id=usuario.id).first()
        if not existe:
            session.add(Publicacion(contenido=row['publicacion'], usuario=usuario))
session.commit()

# Insertar reacciones
for index, row in emociones_df.iterrows():
    usuario = session.query(Usuario).filter_by(nombre=row['usuario']).first()
    publicacion = session.query(Publicacion).filter_by(contenido=row['comentario']).first()
    if usuario and publicacion:
        ya_existe = session.query(Reaccion).filter_by(usuario_id=usuario.id, publicacion_id=publicacion.id).first()
        if not ya_existe:
            session.add(Reaccion(usuario=usuario, publicacion=publicacion, tipo_emocion=row['tipo_emocion']))
session.commit()

print("Datos importados correctamente a la base de datos FutRedX.")

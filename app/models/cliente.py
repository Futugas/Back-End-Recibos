from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes_2'

    id = db.Column(db.Integer, primary_key=True)
    referencia = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.Text)
    lectura_anterior = db.Column(db.Numeric)
    factor = db.Column(db.Numeric, default=1.0)
    cargo = db.Column(db.Numeric, default=0.0)
    estado = db.Column(db.Text, default='operaciones')

    zona_id = db.Column('zona', db.Integer, db.ForeignKey('zonas_2.id'), nullable=False)
    area_id = db.Column('area', db.Integer, db.ForeignKey('areas_2.id'), nullable=False)
    edificio_id = db.Column('edificio', db.Integer, db.ForeignKey('edificios_2.id'), nullable=False)
    departamento_id = db.Column('departamento', db.Integer, db.ForeignKey('departamentos_2.id'), nullable=False)

    # Relación con recibos (si ya tienes el modelo Recibo definido)
    # recibos = db.relationship('Recibo', backref='cliente', cascade='all, delete-orphan')

    precio = db.Column(db.Numeric, default=0.0)
    fecha = db.Column(db.Date, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "referencia": self.referencia,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "lectura_anterior": float(self.lectura_anterior) if self.lectura_anterior else 0,
            "factor": float(self.factor) if self.factor else 1,
            "zona_id": self.zona_id,
            "area_id": self.area_id,
            "edificio_id": self.edificio_id,
            "departamento_id": self.departamento_id,
            "cargo": float(self.cargo) if self.cargo else 0,
            "estado": self.estado,
            "precio": float(self.precio) if self.precio else 0,
            # Se envía como String YYYY-MM-DD o null si está vacía
            "fecha": self.fecha.isoformat() if self.fecha else None
        }
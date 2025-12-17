from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.Text)
    referencia = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(10))

    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)

    recibos = db.relationship(
        'Recibo',
        backref='cliente',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "referencia": self.referencia,
            "codigo_postal": self.codigo_postal,
            "zona_id": self.zona_id,
            "area_id": self.area_id
        }

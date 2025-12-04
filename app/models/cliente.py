from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    direccion = db.Column(db.Text)
    referencia = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(10))

    recibos = db.relationship('Recibo', backref='cliente', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'referencia': self.referencia,
            'codigo_postal': self.codigo_postal
        }

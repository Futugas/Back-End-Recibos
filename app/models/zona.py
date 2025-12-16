from app import db

class Zona(db.Model):
    __tablename__ = 'zonas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    areas = db.relationship('Area', backref='zona', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }


from app import db

class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'zona_id': self.zona_id,
            'nombre': self.nombre
        }

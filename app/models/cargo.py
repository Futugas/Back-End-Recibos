from app import db

class Cargo(db.Model):
    __tablename__ = 'cargos'

    id = db.Column(db.Integer, primary_key=True)
    recibo_id = db.Column(db.Integer, db.ForeignKey('recibos.id'), nullable=False)
    descripcion = db.Column(db.String(200))
    importe = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            'id': self.id,
            'recibo_id': self.recibo_id,
            'descripcion': self.descripcion,
            'importe': float(self.importe) if self.importe else None
        }

from app import db

class Consumo(db.Model):
    __tablename__ = 'consumo'

    id = db.Column(db.Integer, primary_key=True)
    recibo_id = db.Column(db.Integer, db.ForeignKey('recibos.id'), nullable=False)
    lectura_inicial = db.Column(db.Numeric(10, 3))
    lectura_final = db.Column(db.Numeric(10, 3))
    dias_consumo = db.Column(db.Integer)
    consumo_m3 = db.Column(db.Numeric(10, 3))
    factor_conversion = db.Column(db.Numeric(10, 3))
    litros_consumidos = db.Column(db.Numeric(10, 2))
    precio_litro = db.Column(db.Numeric(10, 2))
    consumo_mes = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            'id': self.id,
            'recibo_id': self.recibo_id,
            'lectura_inicial': float(self.lectura_inicial) if self.lectura_inicial else None,
            'lectura_final': float(self.lectura_final) if self.lectura_final else None,
            'dias_consumo': self.dias_consumo,
            'consumo_m3': float(self.consumo_m3) if self.consumo_m3 else None,
            'factor_conversion': float(self.factor_conversion) if self.factor_conversion else None,
            'litros_consumidos': float(self.litros_consumidos) if self.litros_consumidos else None,
            'precio_litro': float(self.precio_litro) if self.precio_litro else None,
            'consumo_mes': float(self.consumo_mes) if self.consumo_mes else None
        }

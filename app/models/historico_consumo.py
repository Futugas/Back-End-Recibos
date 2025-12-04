from app import db

class HistoricoConsumo(db.Model):
    __tablename__ = 'historico_consumo'

    id = db.Column(db.Integer, primary_key=True)
    recibo_id = db.Column(db.Integer, db.ForeignKey('recibos.id'), nullable=False)
    periodo_inicio = db.Column(db.Date)
    periodo_fin = db.Column(db.Date)
    litros = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {
            'id': self.id,
            'recibo_id': self.recibo_id,
            'periodo_inicio': self.periodo_inicio.isoformat() if self.periodo_inicio else None,
            'periodo_fin': self.periodo_fin.isoformat() if self.periodo_fin else None,
            'litros': float(self.litros) if self.litros else None
        }

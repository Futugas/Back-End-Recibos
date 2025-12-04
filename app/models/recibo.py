from app import db

class Recibo(db.Model):
    __tablename__ = 'recibos'
    DELETE_ORPHAN = 'all, delete-orphan'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    numero_recibo = db.Column(db.String(50))
    fecha = db.Column(db.Date)
    periodo_inicio = db.Column(db.Date)
    periodo_fin = db.Column(db.Date)
    precio_autorizado = db.Column(db.Numeric(10, 2))
    precio_apoyo = db.Column(db.Numeric(10, 2))
    total_pagar = db.Column(db.Numeric(10, 2))
    banco = db.Column(db.String(100))
    clabe = db.Column(db.String(25))
    concepto = db.Column(db.String(50))

    consumo = db.relationship('Consumo', backref='recibo', lazy=True, uselist=False, cascade=DELETE_ORPHAN)
    cargos = db.relationship('Cargo', backref='recibo', lazy=True, cascade=DELETE_ORPHAN)
    historico = db.relationship('HistoricoConsumo', backref='recibo', lazy=True, cascade=DELETE_ORPHAN)

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'numero_recibo': self.numero_recibo,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'periodo_inicio': self.periodo_inicio.isoformat() if self.periodo_inicio else None,
            'periodo_fin': self.periodo_fin.isoformat() if self.periodo_fin else None,
            'precio_autorizado': float(self.precio_autorizado) if self.precio_autorizado else None,
            'precio_apoyo': float(self.precio_apoyo) if self.precio_apoyo else None,
            'total_pagar': float(self.total_pagar) if self.total_pagar else None,
            'banco': self.banco,
            'clabe': self.clabe,
            'concepto': self.concepto
        }
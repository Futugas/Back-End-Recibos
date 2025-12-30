from app import db

class Zona(db.Model):
    __tablename__ = 'zonas_2'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    # El relationship necesita que la clase hija tenga el ForeignKey
    areas = db.relationship('Area', backref='zona', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre}

class Area(db.Model):
    __tablename__ = 'areas_2'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # IMPORTANTE: El nombre aquí debe ser el de la TABLA en Postgres (zonas_2)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas_2.id'), nullable=False)

    edificios = db.relationship('Edificio', backref='area', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'zona_id': self.zona_id}

class Edificio(db.Model):
    __tablename__ = 'edificios_2'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas_2.id'), nullable=False)

    departamentos = db.relationship('Departamento', backref='edificio', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'area_id': self.area_id}

class Departamento(db.Model):
    __tablename__ = 'departamentos_2'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edificio_id = db.Column(db.Integer, db.ForeignKey('edificios_2.id'), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nombre': self.nombre, 'edificio_id': self.edificio_id}
import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.cli.command()
def init_db():
    """Inicializar la base de datos"""
    db.create_all()
    print('Base de datos inicializada!')

if __name__ == '__main__':
    app.run()

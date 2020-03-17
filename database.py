from flask_sqlalchemy import SQLAlchemy


class Database:
    """
    This data supports get() and create() calculation history item
    """
    def __init__(self, app):
        db = SQLAlchemy(app)
        self.db = db
        self.db.create_all()
        self.model = calcFactory(db)

    def get(self, id=None):
        if id:
            return self.model.query.get(id)

        all = self.model.query.all()
        if len(all) < 10:
            return all
        return self.model.query[-10:]

    def create(self, ip, text):
        calc = self.model(ip, text)
        self.db.session.add(calc)
        self.db.session.commit()


def calcFactory(db):
    class Calculation(db.Model):
        __tablename__ = 'calculations'
        id = db.Column('id', db.Integer, primary_key=True)
        ip = db.Column(db.String(20))
        text = db.Column(db.String(60))

        def __init__(self, ip, text):
            self.ip = ip
            self.text = text

    return Calculation

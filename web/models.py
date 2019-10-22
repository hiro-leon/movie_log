
from web import db #webディレクトリの__init__.pyからインポート

#db.Modelを継承して、mモデルを作る
class Movie(db.Model):
    #db.Columnでカラムを定義
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    star = db.Column(db.String(64), index=True)
    genre = db.Column(db.String(64), index=True)
    date = db.Column(db.Date)
    recommended = db.Column(db.Integer)
    comment = db.Column(db.String(256))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))


    def __repr__(self):
        return '<Movie {}>'.format(self.title)

class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    extras = db.Column(db.String(128))
    movies = db.relationship('Movie', backref='writer', lazy='dynamic')

    def __repr__(self):
        return '<Director {}>'.format(self.name)
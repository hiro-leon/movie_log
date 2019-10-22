from web import app, db
from flask import render_template, redirect, url_for, request, Blueprint
from web.forms import MovieForm, MovieUpdateForm
from web.models import Movie, Director

# 機能ごとにまとめるためにBluePrintを実装
movies =Blueprint('movies', __name__)

#関数を起動するURLをFlaskインスタンスに教えている89(routeデコレータ)
#ルートディレクトリをブラウザのURL欄に入力するとindex関数が呼び出される
@movies.route('/', methods=['GET'])
def index():
    #クエリとは命令のようなもの
    movies = Movie.query.order_by(Movie.date.desc()).paginate(page=1, per_page=app.config['ITEM_PER_PAGE'], error_out=False)
    directors = db.session.query(Director).join(Movie, Movie.director_id==Director.id).all()
    return render_template('/movies/index.html', movies=movies, directors=directors)

@movies.route('/movies/pages/<int:page_num>', methods=['GET', 'POST'])
def index_pages(page_num):
    movies = Movie.query.order_by(Movie.date.desc()).paginate(page=page_num, per_page=app.config['ITEM_PER_PAGE'], error_out=False)
    directors = db.session.query(Director).join(Movie, Movie.director_id==Director.id).all()
    return render_template('/movies/index.html', movies=movies, directors=directors)


@movies.route('/movies/register', methods=['GET', 'POST'])
def register():

    register_directors = db.session.query(Director).order_by('name')
    directors_list = [(i.id, i.name) for i in register_directors]

    form = MovieForm() #Movieクラスをインスタンス
    form.director.choices = directors_list

    #validate_on_submitメソッドはPOSTリクエスト(この場合register_movie.htmlへの入力)があるかどうか、また、有効なものかどうかを判定する
    if form.validate_on_submit():
        movie = Movie(title=form.title.data,  director_id=form.director.data, star=form.star.data, genre=form.genre.data, date=form.date.data, recommended=form.recommended.data, comment=form.comment.data)
        #movieオブジェクトをデータベースに追加
        db.session.add(movie)
        #movieオブジェクトをデータベースに登録
        db.session.commit()
        #index関数が発動するURLを取得し、移動
        return redirect(url_for('movies.index'))
    return render_template('movies/register.html', form=form)

@movies.route('/movies/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Movie.query.get(id)

    register_directors = db.session.query(Director).order_by('name')
    directors_list = [(i.id, i.name) for i in register_directors]

    form = MovieUpdateForm()
    form.director.choices = directors_list

    if form.validate_on_submit():

        director = db.session.query(Director).filter(Director.id==form.director.data).first()
        movie.title = form.title.data
        movie.director_id = form.director.data
        movie.director = director.name
        movie.star = form.star.data
        movie.genre = form.genre.data
        movie.date = form.date.data
        movie.recommended = form.recommended.data
        movie.comment = form.comment.data
        db.session.commit()
        return redirect(url_for('movies.index'))

    elif request.method=='GET':
        form.title.data = movie.title
        form.director.data = movie.director_id
        form.star.data = movie.star
        form.genre.data = movie.genre
        form.date.data = movie.date
        form.recommended.data = movie.recommended
        form.comment.data = movie.comment

    return render_template('movies/each.html', form=form, id=id)

@movies.route('/movies/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies.index'))
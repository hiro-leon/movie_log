from web import app, db
from web.forms import SearchForm
from web.models import Movie, Director
from flask import render_template, redirect, url_for, request, Blueprint, session
import datetime

searches = Blueprint('searches', __name__)

@searches.route('/searches/', methods=['GET','POST'])
def index_search():

    registered_directors = db.session.query(Director).order_by('name')
    directors_list = [(0, "")]
    for i in registered_directors:
        directors_list.append([i.id, i.name])

    form = SearchForm()
    form.director.choices = directors_list

    if form.start_date.data is None:
        form.start_date.data = datetime.date(datetime.datetime.today().year, 1, 1)
    if form.end_date.data is None:
        form.end_date.data = datetime.datetime.today()

    if form.validate_on_submit():

        if form.director.data != 0:
            movies = Movie.query.filter(Movie.title.like('%' + form.title.data + '%')).filter(
                Movie.director_id == form.director.data).filter(Movie.date >= form.start_date.data).filter(
                Movie.date <= form.end_date.data)
        else:
            movies = Movie.query.filter(Movie.title.like('%' + form.title.data + '%')).filter(Movie.date>=form.start_date.data).filter(Movie.date<=form.end_date.data)

        movies = movies.order_by(Movie.date.desc()).paginate(page=1, per_page=app.config['ITEM_PER_PAGE'],error_out=False)
        directors = db.session.query(Director).join(Movie, Movie.director_id == Director.id).all()

        #sessionはクッキーを用いて、情報をブラウザ上に保存する
        session['title'] = form.title.data
        session['director'] = form.director.data
        session['start_date'] = form.start_date.data.strftime('%Y-%m-%d')
        session['end_date'] = form.end_date.data.strftime('%Y-%m-%d')

        return render_template('searches/search_results.html', movies=movies, directors=directors)
    return render_template('searches/search.html', form=form)



@searches.route('/searches/<int:page_num>', methods=['GET', 'POST'])
def search_results(page_num):
    form = SearchForm()

    form.title.data=session.get('title')
    form.director.data=session.get('director')
    form.start_date.data=datetime.datetime.strptime(session.get('start_date'), '%Y-%m-&d')
    form.end_date.data=datetime.datetime.strptime(session.get('end_date'), '%Y-%m-%d')

    if form.director.data != 0:
        movies=Movie.query.filter(Movie.title.like('%' + 'form.title.data' + '%')).filter(Movie.director_id==form.director.data).filter(Movie.date>=form.start_date.data).filter(Movie.date<=form.end_date.data)
    else:
        movies = Movie.query.filter(Movie.title.like('%' + 'form.title.data' + '%')).filter(Movie.date >= form.start_date.data).filter(Movie.date <= form.end_date.data)
    movies=movies.order_by(Movie.data.desc()).paginate(page=page_num, per_page=app.config['ITEM_PER_PAGE'], error_out=False)
    directors=db.session.query(Director).join(Movie, Movie.director_id==Director.id).all()

    return render_template('/searches/search_results.html', movies=movies, directors=directors)
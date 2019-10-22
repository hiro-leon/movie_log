from web import app, db
from flask import render_template, redirect, url_for, request, Blueprint
from web.forms import DirectorForm, DirectorUpdateForm
from web.models import Director, Movie


directors =Blueprint('directors', __name__)

#ルートディレクトリをブラウザのURL欄に入力するとindex関数が呼び出される
@directors.route('/directors', methods=['GET'])
def index():
    directors = Director.query.order_by(Director.name).paginate(page=1, per_page=app.config['DIRECTORS_PER_PAGE'], error_out=False)
    #movies = [{'title':'leon', 'director':'ko', 'star':'dd'}]
    return render_template('/directors/index.html', directors=directors)

@directors.route('/directors/pages/<int:page_num>', methods=['GET', 'POST'])
def index_pages(page_num):
    directors = Director.query.order_by(Director.name).paginate(page=page_num, per_page=app.config['DIRECTORS_PER_PAGE'], error_out=False)
    return render_template('/directors/index.html', directors=directors)


@directors.route('/directors/register', methods=['GET', 'POST'])
def register():
    form = DirectorForm()

    if form.validate_on_submit():
        check = Director.query.filter(Director.name == form.name.data).first()
        if check:
            errors = 'この監督はすでに登録されています。他の監督を登録してください。'
            return render_template('directors/register.html', form=form, errors=errors)

        director = Director(name=form.name.data, extras=form.extras.data)
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('directors.index'))
    return render_template('directors/register.html', form=form)

@directors.route('/directors/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    director = Director.query.get(id)

    form = DirectorUpdateForm()

    if form.validate_on_submit():
        check = Director.query.filter(Director.name == form.name.data).first()
        if check:
            errors = 'この監督はすでに登録されています。他の監督を登録してください。'
            return render_template('directors/register.html', form=form, errors=errors)

        director.name  = form.name.data
        director.extras = form.extras.data
        db.session.commit()
        return redirect(url_for('directors.index'))

    elif request.method=='GET':
        form.name.data = director.name
        form.extras.data = director.extras

    return render_template('directors/each.html', form=form, id=id)


@directors.route('/directors/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    director = Director.query.get(id)
    check = Movie.query.filter(Movie.director_id == id).first()
    if check:
        errors = 'この監督による映画を先に削除してください'
        form = DirectorForm()
        form.name.data = director.name
        form.extras.data = directors.extras
        return render_template('directors/each.html', form=form, id=id, errors=errors)

    db.session.delete(director)
    db.session.commit()
    return redirect(url_for('directors.index'))
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('映画タイトル', validators=[DataRequired()]) #DataRequiredは必ずデータの入力が必要
    director = SelectField('監督', coerce=int, validators=[DataRequired()])
    star = StringField('主演')
    genre = SelectField('ジャンル', choices=[('ドラマ','ドラマ'),('アクション','アクション'),('ホラー','ホラー'),('ラブストーリー','ラブストーリー')])
    date = DateField('鑑賞日', format="%Y-%m-%d")
    recommended = SelectField('おすすめ度', choices=[('5', '5:とてもおすすめ'), ('4', '4:ややおすすめ'), ('3', '3:普通'), ('2', '2:あまりおすすめしない'), ('1', '1:全くおすすめしない')])
    comment = TextAreaField('コメント')
    submit = SubmitField('登録')

class DirectorForm(FlaskForm):
    name = StringField('監督', validators=[DataRequired()])
    extras = StringField('説明')
    submit = SubmitField('登録')


class MovieUpdateForm(MovieForm):
    submit = SubmitField('修正')

class DirectorUpdateForm(DirectorForm):
    submit = SubmitField('修正')

class SearchForm(FlaskForm):
    title = StringField('映画')
    director = SelectField('監督', coerce=int)
    start_date = DateField('検索開始日', format="%Y-%m-%d")
    end_date = DateField('検索終了日', format="%Y-%m-%d")
    submit = SubmitField('検索')

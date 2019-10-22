from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #コマンドラインによるデータベース操作が可能

#Flaskのアプリケーションオブジェクト
#Flaskをappという名前でインスタンス化
app = Flask(__name__)
app.config.from_object(Config)
#データベースをインスタンス化
db =SQLAlchemy(app)
migrate = Migrate(app, db)

from web.movies.views import movies
from web.directors.views import directors
from web.searches.views import searches
#それぞれのviewsで実装したblueprintをアプリケーションに登録(一度登録したら解除の関数はないので解除不能になる)
app.register_blueprint(movies)
app.register_blueprint(directors)
app.register_blueprint(searches)

#これで、http://xxx/movies/register、http://xxx/directors/...、http://xxx/searches/.. にアクセスできるようになる。


#コマンドラインにflask db initでデータベースのテーブル作成
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, default=datetime.today())
    def __repr__(self):
        return '<Movie %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/create_movie', methods=['POST', 'GET'])
def create_movie():
    if request.method == "POST":
        title = request.form['title']
        if not title or title.split() == []:
            return render_template("create_movie.html", extra_info="! Укажите название !")
        try:
            release_date = datetime.fromisoformat(request.form['release_date'])
        except:
            return render_template("create_movie.html", title=title, extra_info="! Укажите дату !")
        movie = Movie(title=title, release_date=release_date)

        db.session.add(movie)
        db.session.commit()
        return redirect('/')

    else:
        return render_template("create_movie.html")

@app.route('/movie_list')
def get_movie_list():
    movies = Movie.query.order_by(Movie.release_date.desc()).all()
    return render_template("movie_list.html", movies=movies)

@app.route('/movie_list/<int:id>')
def post_detail(id):
    movie = Movie.query.get(id)
    if movie == None:
        return render_template("not_found.html")
    return render_template("movie_detail.html", movie=movie)

@app.route('/movie_list/<int:id>/movie_update', methods=['POST', 'GET'])
def movie_update(id):
    movie = Movie.query.get(id)
    if movie == None:
        return render_template("not_found.html")

    if request.method == "POST":
        title = request.form['title']
        if not title or title.split() == []:
            return render_template("movie_update.html", movie=movie, extra_info="! Укажите название !")
        movie.title = title
        movie.release_date = datetime.fromisoformat(request.form['release_date'])
        try:
            db.session.commit()
            return redirect('/movie_list')
        except:
            return "При редактировании возникла ошибка"
    else:
        return render_template("movie_update.html", movie=movie)

@app.route('/movie_list/<int:id>/movie_delete')
def movie_delete(id):
    movie = Movie.query.get(id)
    if movie == None:
        return render_template("not_found.html")

    try:
        db.session.delete(movie)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении возникла ошибка"

if __name__ == "__main__":
    app.run(debug=True)
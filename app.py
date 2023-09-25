from flask import Flask ,request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/catalog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
app.app_context().push()
#with app.app_context():
#db.create_all()

@app.route('/')
def helloworld():
  return "hello world"
@app.route('/new/')
def string_query(greeting ='hello'):
  valu_query = request.args.get('greeting',greeting)
  return '<h1>the greeting is :{0}</h1>'.format(valu_query)  
@app.route('/user/<name>')
def no_string_query(name='chaimae'):
  return '<h1>hello dear :{}</h1>'.format(name)
@app.route('/index/')
def tem():
  return render_template('index.html')

@app.route('/movie')
def movies():
  movie_list =['me befour you',
               'the holiday',
               'call soule god man',
               'breaking bad']
  return render_template('movies.html',movies=movie_list)


@app.route('/table')
def moviesdata():
  movie_list ={'me befour you': 2.1,
               'the holiday': 1.1,
               'call soule god man': 3.3,
               'breaking bad': 4}
  return render_template('tables_data.html',movies = movie_list)

@app.route('/filter')
def movies_filter():
   movies_list = {'me befour you': 3.1,
                 'the holiday': 1.1,
                 'call soule god man': 3.3,
                 'breaking bad': 4}
   return render_template('filters_data.html',movies = movies_list,name=None ,film ='a christmas carol')

@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('using_macros.html', movies=movies_dict)

# PUBLICATION TABLE
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Name is {}'.format(self.name)
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH A RELATIONSHIP BETWEEN PUBLICATION AND BOOK TABLES
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)

if __name__ == "__main__" :
 with app.app_context():
  db.create_all() 
 app.run(host="0.0.0.0" ,debug =True )

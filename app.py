from flask import Flask, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    port = 9095
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0258@localhost/feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://'


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    cat = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, email, cat, rating, comments):
        self.customer = customer
        self.email = email
        self.cat = cat
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html', title='HOME')


@app.route('/rate')
def rate():
    return render_template('rate.html', title='RATING PAGE')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        cat = request.form['cat']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, email, cat, rating, comments)
        if customer == '' or cat == '' or email == '':
            return render_template('rate.html', message='please enter required fields***')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, email, cat, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, email, cat, rating, comments)
            return render_template('success.html', title='Success', **locals())
        return render_template('rate.html', message='You have already submitted feedback with this Username')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True, port=9095)


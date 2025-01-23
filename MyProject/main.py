from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'{self.username}'

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['userName']
        password = request.form['exampleInputPassword1']
        
        # Check if the username already exists
        existing_user = Form.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('home'))
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Create a new user entry
        new_user = Form(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully registered.', 'success')
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again later.", 'danger')

    allForms = Form.query.all()  # This is just for debug, if you want to list all users
    return render_template('index.html', allForms=allForms)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Database created successfully')
    app.run(debug=True)

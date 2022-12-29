# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms.validators import DataRequired, Email, EqualTo
from forms import UpdateCourseForm, UpdateVideoForm, AddCourseForm, LoginForm, RegisterForm
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

# Load user
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    if user:
        return User(user[0], user[1], user[2])
    return None


# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', email=current_user.email, username=current_user.username)

# app.py (continued)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error=""
    if form.validate_on_submit():
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (form.username.data, form.password.data))
        user = c.fetchone()
        if user:
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            return redirect(url_for('profile'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('courses'))
    else:
        if form.validate_on_submit():
            if form.password.data != form.confirm_password.data:
                return "Passwords do not match"
            conn = sqlite3.connect('mydatabase.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (form.username.data, form.email.data, form.password.data))
            conn.commit()
            c.close()
            conn.close()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/courses')
@login_required
def courses():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name, description FROM courses")
    courses = c.fetchall()
    course_objs = []
    for course in courses:
        c.execute("SELECT * FROM videos WHERE course_id=?", (course[0],))
        videos = c.fetchall()
        course_objs.append({
            "name": course[0],
            "desc" : course[1],
        })
    return render_template('courses.html', courses=course_objs)

# app.py (continued)
@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['description']
        iframe = request.form['iframes_links']
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO courses (name, description, iframes_links) VALUES (?,?,?)", (name, desc, iframe))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('courses'))
    form = AddCourseForm()
    return render_template('add_course.html', form=form)

@app.route('/courses/<name>')
@login_required
def view_course(name):
    # Connect to the database
    search = name
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Fetch the iframe links for the course
    c.execute("SELECT * FROM courses WHERE name=?", (search,))
    links = c.fetchall()
    c.close()
    # Render the template with the iframe links
    return render_template('view_course.html', links=links, title=search)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()

        c.execute("INSERT INTO reviews (name, email, message) VALUES (?,?,?)", (name, email, message))
        c.close()
        conn.close()

        return render_template('contact.html', msg="Message Sent..!!")
    else:
        return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
    
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/dmca')
def dmca():
    return render_template('DMCA.html')

'''@app.route('/update_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    form_id = course_id.id.data
    course_id = int(form_id)
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE id=?", (course_id,))
    course = c.fetchone()
    form = UpdateCourseForm()
    if form.validate_on_submit():
        name = form.name.data
        c.execute("UPDATE courses SET name=? WHERE id=?", (name, course_id))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('courses'))
    return render_template('update_course.html', course=form)'''

@app.route('/delete_course/<course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("DELETE FROM courses WHERE id=?", (course_id,))
    conn.commit()
    c.close()
    conn.close()
    print("Deleted")
    return redirect(url_for('courses'))

@app.route('/reset', methods=["GET","POST"])
@login_required
def reset():
    if request.method == 'POST':
        new_pass = request.form['new_pass']
        email = request.form['email']
        username = current_user.username
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND email = ?', (username, email))
        user = c.fetchone()

        if user is None:
            return render_template('reset.html', msg="please input correct email")

        c.execute("UPDATE users SET password=? WHERE username=? AND email=?", (new_pass,username,email))
        conn.commit()
        c.close()
        conn.close()
        msg="sucess"
        return render_template('reset.html', msg=msg)
    else:
        return render_template('reset.html')

@app.route('/add_video/<int:course_id>', methods=['GET', 'POST'])
@login_required
def add_video(course_id):
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()
        c.execute("INSERT INTO videos (course_id, title, link) VALUES (?, ?, ?)", (course_id, title, link))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('courses'))
    return render_template('add_video.html')

# app.py (continued)
@app.route('/update_video/<int:video_id>', methods=['GET', 'POST'])
@login_required
def update_video(video_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("SELECT * FROM videos WHERE id=?", (video_id,))
    video = c.fetchone()
    form = UpdateVideoForm(title=video[2], link=video[3])
    if form.validate_on_submit():
        title = form.title.data
        link = form.link.data
        c.execute("UPDATE videos SET title=?, link=? WHERE id=?", (title, link, video_id))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('courses'))
    return render_template('update_video.html', form=form)

@app.route('/delete_video/<int:video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute("DELETE FROM videos WHERE id=?", (video_id,))
    conn.commit()
    c.close()
    conn.close()
    return redirect(url_for('courses'))

if __name__ == '__main__':
    app.run(debug=True)

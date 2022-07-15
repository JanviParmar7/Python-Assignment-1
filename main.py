from flask import Flask, render_template, request, redirect, url_for, session
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import psycopg2
import psycopg2.extras
import datetime




app = Flask(__name__)
app.secret_key = "jignasa-chavda12"



DB_HOST = "localhost"
DB_NAME = "employee"
DB_USER = "postgres"
DB_PASS = "test123"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

PHOTO_FOLDER = 'static/profile/'
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_A'] = PHOTO_FOLDER



@app.route('/')
def Index():
    if 'checklogin' in session:
        return redirect(url_for('display'))
    elif 'chkuserlogin' in session:
        return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('adminlogin'))


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    cur = conn.cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cur.execute(f"SELECT * FROM admin_login WHERE email='{email}' AND passwd='{password}'")
        account = cur.fetchone()

        cur.execute(f"SELECT * FROM user_login WHERE email='{email}'")
        data = cur.fetchone()

        if account:
            session['checklogin'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            session['password'] = account[2]
            session['username'] = account[3]
            flash(u'You have successfully logged in!')
            return redirect(url_for('display'))
        elif data:
            password_rs = data[3]
            check = check_password_hash(password_rs, password)
            if check:
                session['chkuserlogin'] = True
                session['id'] = data[0]
                session['username'] = data[2]
                session['email'] = data[1]
                session['password'] = data[3]
                flash(u'You have successfully logged in!')
                return redirect(url_for('userprofile'))


            else:
                err = "Incorrect username/password"
                return render_template('admin_login.html', err=err)
        else:
            error = "Incorrect username/password"
            return render_template('admin_login.html', error=error)

    cur.close()
    return render_template('admin_login.html')


@app.route('/user-profile')
def userprofile():
    if session['chkuserlogin']:
        cur = conn.cursor()
        user_id = session['id']
        cur.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id ='{user_id}' and user_profile.user_id='{user_id}'")
        data = cur.fetchone()
        return render_template("user_profile.html", data=data)
    else:
        return render_template("admin_login.html")


@app.route('/adminmaster', methods=["GET", "POST"])
def display():
    if session['checklogin']:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = user_profile.user_id order by user_login.id desc")
        account = cur.fetchall()
        return render_template("admin_master.html", data=account)
    else:
        return render_template("admin_login.html")


@app.route("/update-user-profile/<int:user_id>")
def fetch_update_user(user_id):
    if session['checklogin']:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM user_profile, user_login WHERE user_login.id = '{user_id}' and user_profile.user_id = '{user_id}'")
        account = cur.fetchone()
        cur.close()
        return render_template("edit.html", account=account)
    else:
        return redirect(url_for('admin_login'))


@app.route("/update", methods=["GET", "POST"])
def update():
    if session['checklogin']:
        if request.method == "POST":

            user_id = request.form.get("userid")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            dob = request.form.get("dob")
            mobile = request.form.get("mobile")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            username = request.form.get("username")
            email = request.form.get("email")
            date_modified = datetime.date.today()
            cur = conn.cursor()

            cur.execute(f"""UPDATE user_profile set first_name='{fname}', last_name='{lname}', date_of_birth='{dob}',
                                    mobile_number='{mobile}', gender='{gender}', address='{address}', city='{city}',
                                    state='{state}', zipcode='{zipcode}', profile_updated_dt='{date_modified}' WHERE user_id='{user_id}'""")
            cur.execute(f"""UPDATE user_login set username='{username}', email='{email}' WHERE id='{user_id}'""")
            conn.commit()
            cur.close()
        flash(u'Information updated successfully!')
        return redirect(url_for('display'))
    else:
        return redirect(url_for('adminlogin'))


@app.route("/delete/<int:user_id>")
def delete(user_id):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM user_profile where user_id ='{user_id}'")
    cur.execute(f"DELETE FROM user_login WHERE id ='{user_id}'")
    conn.commit()
    cur.close()
    return redirect(url_for('display'))


@app.route('/resetpw/<int:user_id>')
def resetpw(user_id):
    if session['checklogin']:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}'and user_profile.user_id = '{user_id}'")
        account = cur.fetchone()
        print(account)

        return render_template("change_password.html", account=account)
    else:
        return redirect(url_for('display'))


@app.route('/newpw/<int:user_id>', methods=["GET", "POST"])
def newpw(user_id):
    if session['checklogin']:
        password = request.form.get('newpassword')
        confirmpw = request.form.get('confirmpw')
        if request.method == "POST":
            if password == confirmpw:
                confirm_pw()

            else:
                error = "Password and Confirm password doesn't match..."
                cur = conn.cursor()
                cur.execute(
                    f"SELECT * FROM user_profile,user_login where user_login.id = '{user_id}'and user_profile.user_id = '{user_id}'")
                account = cur.fetchone()
                return render_template("change_password.html", account=account, error=error)
    else:
        return redirect(url_for('adminlogin'))
    return redirect(url_for('display'))


def confirm_pw():
    cur = conn.cursor()
    user_id = request.form.get("user_id")
    password = request.form.get("newpassword")
    hash_pwd = generate_password_hash(password)
    cur.execute(f"UPDATE user_login set passwd='{hash_pwd}' WHERE id='{user_id}'")
    conn.commit()
    cur.close()
    flash(u'Password Changed successfully!')
    return redirect(url_for('display'))


@app.route("/adduser", methods=["GET", "POST"])
def adduser():
    return render_template("add_user.html")


@app.route("/extra", methods=["GET", "POST"])
def extra():
    return render_template("extra2.html")


@app.route("/createuser", methods=["GET", "POST"])
def createuser():
    if session['checklogin']:
        cur = conn.cursor()
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_pw = request.form.get('confirm_pw')
        cur.execute(f"select * from user_login where email='{email}'")
        user_exists = cur.fetchone()
        cur.close()
        if user_exists:
            msg = "Account with this email already exists, Please try another email!"
            return render_template("add_user.html", error=msg)
        if request.method == "POST":
            if password == confirm_pw:
                newuser()
            else:
                msg = "Password and Confirm password doesn't match..."
                return render_template("add_user.html", error=msg)
    else:
        return redirect(url_for('adminlogin'))
    return redirect(url_for('display'))


def newuser():
    cur = conn.cursor()
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hash_pwd = generate_password_hash(password)
    cur.execute(f"""INSERT INTO user_login (username,email,passwd) VALUES('{username}','{email}','{hash_pwd}')""")
    conn.commit()
    cur.execute("SELECT max(id) FROM user_login")
    new_id = cur.fetchone()
    cur.execute(
        f"""INSERT INTO user_profile (user_id) VALUES ('{new_id[0]}')""")
    conn.commit()
    cur.close()
    flash(u'User Created Successfully!')
    return redirect(url_for('display'))


@app.route("/update-user-profile/user_id", methods=["GET", "POST"])
def fetch_user_edit():
    user_id = session['id']
    if session['chkuserlogin']:
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM user_profile, user_login WHERE user_login.id = '{user_id}' and user_profile.user_id = '{user_id}'")
        data = cur.fetchone()
        cur.close()
        return render_template("user_edit.html", data=data)
    else:
        return redirect(url_for('admin_login'))



@app.route("/update_user", methods=["GET", "POST"])
def updateuser():
    if session['chkuserlogin']:
        if request.method == "POST":
            user_id = request.form.get("userid")
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            dob = request.form.get("dob")
            mobile = request.form.get("mobile")
            gender = request.form.get("gender")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            zipcode = request.form.get("zipcode")
            username = request.form.get('username')
            email = request.form.get('email')
            file = request.files['photo']
            pdffile = request.files['pdf']
            date_modified = datetime.date.today()
            cur = conn.cursor()
            if request.method == "POST":
                pdfnm = secure_filename(pdffile.filename)
                filename = secure_filename(file.filename)
                pdffile.save(os.path.join(app.config['UPLOAD_FOLDER'], pdfnm))
                file.save(os.path.join(app.config['UPLOAD_FOLDER_A'], filename))
            cur.execute(f"UPDATE user_profile set first_name='{fname}', last_name='{lname}', date_of_birth='{dob}', mobile_number='{mobile}', gender='{gender}', address='{address}', city='{city}', state='{state}', zipcode='{zipcode}', profile_updated_dt='{date_modified}', img='{filename}', birth_certificate='{pdfnm}'  WHERE user_id='{user_id}'")
            cur.execute(
                f"UPDATE user_login set username='{username}', email='{email}'WHERE id='{user_id}'")
            conn.commit()
            cur.close()
            flash(u'Your profile updated successfully')
        return redirect(url_for('userprofile'))
    else:
        return redirect(url_for('adminlogin'))



@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='upload/' + filename))


@app.route("/logout")
def logout_admin():
    session['checklogin'] = False
    session.clear()
    return render_template("admin_login.html")


@app.route("/logout")
def logout_user():
    session['chkuserlogin'] = False
    session.clear()
    return render_template("admin_login.html")


if __name__ == "__main__":
    app.run(debug=True)


import json
from flask import Flask, render_template, flash, url_for, redirect
from forms import passwdchangeform, registerform
from model import reset_passwd, new_user, reset_pwd_user
import ssl

file = open("src/config.json")
variables = json.loads(file.read())

app = Flask(__name__)
app.config['SECRET_KEY'] = variables['SECRET_KEY_FLASK']
app.config['RECAPTCHA_PUBLIC_KEY'] = variables['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = variables['RECAPTCHA_PRIVATE_KEY']
app.config['TESTING'] = variables['debug']
domain = variables['domain']
domain_name = variables['domain_name']
BASEDN = variables['BASEDN']
user_admin = variables['user_admin']
passwd_admin = variables['passwd_admin']


@app.route("/", methods=['GET', 'POST'])
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    form = passwdchangeform()
    if form.validate_on_submit():

        if reset_passwd(domain, user_admin, passwd_admin, BASEDN, str(form.username.data), str(form.password.data), str(form.new_password.data), domain_name, enable=False):
            flash(u'Your password was changed for:' +
                  str(form.username.data), category='success')
            return redirect(url_for('reset'))
        else:
            flash(u'Not possible reset the password for:' +
                  str(form.username.data) + ' please contact system admin', category='danger')
            return redirect(url_for('reset'))
   
    return render_template('reset.html', title='AD Password Reset' + variables['company'], form=form, company=variables['company'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registerform()
    user = {
        "username": form.username.data,
        "firstname": form.firstname.data,
        "lastname": form.lastname.data,
        "idcard": form.idcard.data,
        "password": form.password.data,
        "telephone": form.telephone.data,
        "mobile": form.mobile.data,
        "email": form.email.data,
        "level": form.level.data,
        "department": form.department.data,
        "branch": form.branch.data,
        "office": form.office.data,
        "position": form.position.data
    }
    if form.validate_on_submit():
        if new_user(domain, user_admin, passwd_admin, BASEDN, domain_name, user):
            flash(u'Your registered for:' +
                  str(form.username.data), category='success')
            return redirect(url_for('register'))
        else:
            flash(u'Not possible register for: ' +
                  str(form.username.data) + ' please contact system admin', category='danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='AD Password Reset' + variables['company'], form=form, company=variables['company'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=variables['debug'], host='0.0.0.0', port=5001)

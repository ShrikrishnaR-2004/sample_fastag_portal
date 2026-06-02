from flask import Blueprint, render_template, redirect, url_for, request, flash

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.login'))


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/signup')
def signup():
    return render_template('signup.html')


@main.route('/send-otp', methods=['POST'])
def send_otp():
    phone = request.form.get('phone', '')
    last4 = phone[-4:] if len(phone) >= 4 else phone
    return redirect(url_for('main.otp_verify', phone=last4))


@main.route('/otp-verify')
def otp_verify():
    phone = request.args.get('phone', '****')
    return render_template('otp_verify.html', phone=phone)


@main.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')


@main.route('/reset-password')
def reset_password():
    return render_template('reset_password.html')


@main.route('/reset-success')
def reset_success():
    return render_template('reset_success.html')


@main.route('/mpin-setup')
def mpin_setup():
    return render_template('mpin_setup.html')

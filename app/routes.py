import hashlib
import hmac
import secrets
from datetime import datetime, timezone, timedelta
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, session, current_app, make_response
)
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
from .models import User, PasswordResetToken, PasswordHistory, Wallet, Vehicle
from .forms import (
    LoginForm, SignupForm, OtpVerifyForm, MpinSetupForm,
    ForgotPasswordForm, ResetPasswordForm
)
from .services.otp_service  import generate_otp, send_otp_sms
from .services.mail_service import send_reset_email
from .services.captcha_service import generate_captcha_text, generate_captcha_svg

main = Blueprint('main', __name__)

def _hash_aadhaar(raw: str, pepper: str) -> str:
    """HMAC-SHA256 of the raw 12-digit Aadhaar using a secret pepper."""
    return hmac.new(pepper.encode('utf-8'), raw.encode('utf-8'), hashlib.sha256).hexdigest()

def _hash_pan(raw: str, pepper: str) -> str:
    """HMAC-SHA256 of the normalised PAN using a secret pepper."""
    return hmac.new(pepper.encode('utf-8'), raw.encode('utf-8'), hashlib.sha256).hexdigest()

def _normalise_phone(phone: str) -> str:
    return phone.replace(' ', '').strip()

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/captcha/image')
def captcha_image():
    """Generates an SVG captcha and stores the text in session."""
    text = generate_captcha_text()
    session['captcha_text'] = text
    svg = generate_captcha_svg(text)
    
    response = make_response(svg)
    response.content_type = 'image/svg+xml'
    # Prevent caching
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = LoginForm()
    
    if form.validate_on_submit():
        # Validate Captcha
        expected_captcha = session.get('captcha_text', '')
        if not expected_captcha or form.captcha.data.upper() != expected_captcha.upper():
            flash('Invalid captcha code. Please try again.', 'danger')
            return render_template('login.html', form=form)
            
        phone = _normalise_phone(form.mobile.data)
        user  = User.query.filter_by(phone=phone).first()
        
        if user and user.check_password(form.password.data):
            # Clear captcha from session after success
            session.pop('captcha_text', None)
            
            login_user(user)
            flash(f'Welcome back, {user.full_name.split()[0]}! 👋', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
            
        session['login_fails'] = session.get('login_fails', 0) + 1
        flash('Invalid mobile number or password.', 'danger')
        
    return render_template('login.html', form=form)
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.login'))
@main.route('/dashboard')
@login_required
def dashboard():
    # Pass dynamic backend data and some mock financial info for the dashboard
    stats = {
        'no_of_tags': current_user.vehicles.count(),
        'threshold_limit': current_user.wallet.threshold_limit if current_user.wallet else 100.00,
        'monthly_limit': current_user.wallet.monthly_limit if current_user.wallet else 200000.00,
        'wallet_balance': current_user.wallet.balance if current_user.wallet else 0.00,
        'security_deposit': current_user.wallet.security_deposit if current_user.wallet else 200.00
    }
    
    vehicles = current_user.vehicles.all()
        
    now_str = datetime.now().strftime("%a, %d %b %Y")
    return render_template('dashboard.html', user=current_user, stats=stats, vehicles=vehicles, now=now_str)
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        # Validate Captcha
        expected_captcha = session.get('captcha_text', '')
        if not expected_captcha or form.captcha.data.upper() != expected_captcha.upper():
            flash('Invalid captcha code. Please try again.', 'danger')
            return render_template('signup.html', form=form)
            
        phone = _normalise_phone(form.phone.data)
        if User.query.filter_by(phone=phone).first():
            flash('A FASTag account with this mobile number already exists. Please sign in.', 'danger')
            return render_template('signup.html', form=form)
        if User.query.filter_by(email=form.email.data.lower().strip()).first():
            flash('An account with this email address already exists.', 'danger')
            return render_template('signup.html', form=form)
        today = datetime.today().date()
        dob   = form.dob.data
        age   = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            flash('You must be at least 18 years old to register.', 'danger')
            return render_template('signup.html', form=form)
        pepper = current_app.config['KYC_PEPPER']
        user = User(
            full_name    = form.full_name.data.strip(),
            phone        = phone,
            email        = form.email.data.lower().strip(),
            dob          = dob,
            pan_hash     = _hash_pan(form.pan.data.upper().strip(), pepper) if form.pan.data else None,
            vehicle_reg  = form.vehicle_reg.data.upper().replace(' ', '') if form.vehicle_reg.data else None,
            vehicle_type = form.vehicle_type.data or None,
            permit_rc    = form.permit_rc.data.strip() if form.permit_rc.data else None,
        )
        aadhaar_raw = (form.aadhaar.data or '').replace(' ', '').replace('•', '')
        if aadhaar_raw and len(aadhaar_raw) == 12:
            user.aadhaar_hash = _hash_aadhaar(aadhaar_raw, pepper)
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = pw_hash
        db.session.add(user)
        db.session.flush()          # user.id is now assigned by the DB
        
        history = PasswordHistory(user_id=user.id, password_hash=pw_hash)
        db.session.add(history)
        
        # Create a wallet for the new user
        wallet = Wallet(user_id=user.id)
        db.session.add(wallet)
        
        # If user registered a vehicle, add it
        if user.vehicle_reg:
            vehicle = Vehicle(
                user_id=user.id,
                vehicle_number=user.vehicle_reg,
                vehicle_class=user.vehicle_type or 'Car/Jeep/Van(VC4)',
                is_commercial=False,
                status='Active'
            )
            db.session.add(vehicle)
        
        db.session.commit()
        otp = generate_otp()
        session['otp_code']    = otp
        session['otp_phone']   = phone
        session['otp_user_id'] = user.id
        session['otp_expires'] = (
            datetime.now(timezone.utc) +
            timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])
        ).isoformat()
        send_otp_sms(phone, otp)
        return redirect(url_for('main.otp_verify', phone=phone[-4:]))
    if form.errors and request.method == 'POST':
        for field, errs in form.errors.items():
            for err in errs:
                flash(err, 'danger')
    return render_template('signup.html', form=form)
@main.route('/send-otp', methods=['POST'])
def send_otp():
    phone = _normalise_phone(request.form.get('phone', ''))
    if not phone:
        flash('Please enter a valid mobile number.', 'danger')
        return redirect(url_for('main.signup'))
    otp = generate_otp()
    session['otp_code']    = otp
    session['otp_phone']   = phone
    session['otp_expires'] = (
        datetime.now(timezone.utc) +
        timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])
    ).isoformat()
    send_otp_sms(phone, otp)
    return redirect(url_for('main.otp_verify', phone=phone[-4:]))
@main.route('/otp-verify', methods=['GET', 'POST'])
def otp_verify():
    phone = request.args.get('phone', '****')
    if request.method == 'POST':
        otp_entered = request.form.get('otp_combined', '')
        if not otp_entered:
            digits = [request.form.get(f'otp_{i}', '') for i in range(1, 7)]
            otp_entered = ''.join(digits)
        stored_otp     = session.get('otp_code', '')
        stored_expires = session.get('otp_expires', '')
        user_id        = session.get('otp_user_id')
        expired = False
        if stored_expires:
            exp_dt  = datetime.fromisoformat(stored_expires)
            expired = datetime.now(timezone.utc) > exp_dt
        if expired:
            flash('OTP has expired. Please request a new one.', 'danger')
            return render_template('otp_verify.html', phone=phone)
        if otp_entered == stored_otp:
            if user_id:
                user = User.query.get(user_id)
                if user:
                    user.is_phone_verified = True
                    db.session.commit()
                    login_user(user)
            session.pop('otp_code',    None)
            session.pop('otp_phone',   None)
            session.pop('otp_expires', None)
            flash('Mobile number verified successfully! 🎉', 'success')
            return redirect(url_for('main.mpin_setup'))
        else:
            flash('Incorrect OTP. Please try again.', 'danger')
    return render_template('otp_verify.html', phone=phone)
@main.route('/mpin-setup', methods=['GET', 'POST'])
@login_required
def mpin_setup():
    form = MpinSetupForm()
    if form.validate_on_submit():
        current_user.set_mpin(form.mpin.data)
        db.session.commit()
        logout_user()
        flash('Successfully signed up!', 'success')
        return redirect(url_for('main.login'))
    if form.errors and request.method == 'POST':
        for field, errs in form.errors.items():
            for err in errs:
                flash(err, 'danger')
    return render_template('mpin_setup.html', form=form)
@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user  = User.query.filter_by(email=email).first()
        if user:
            PasswordResetToken.query.filter_by(user_id=user.id, used=False).delete()
            token     = secrets.token_urlsafe(48)
            expiry_dt = datetime.now(timezone.utc) + timedelta(
                minutes=current_app.config.get('RESET_TOKEN_EXPIRY_MINUTES', 30)
            )
            reset_tok = PasswordResetToken(
                user_id    = user.id,
                token      = token,
                expires_at = expiry_dt,
            )
            db.session.add(reset_tok)
            db.session.commit()
            send_reset_email(user, token)
        flash('If that email is registered, a reset link has been sent.', 'info')
        return redirect(url_for('main.forgot_password'))
    return render_template('forgot_password.html', form=form)
@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    tok_record = PasswordResetToken.query.filter_by(token=token).first()
    if not tok_record or not tok_record.is_valid:
        flash('This reset link is invalid or has expired. Please request a new one.', 'danger')
        return redirect(url_for('main.forgot_password'))
    form = ResetPasswordForm()
    user = tok_record.user
    if form.validate_on_submit():
        limit = current_app.config.get('PASSWORD_HISTORY_LIMIT', 3)
        if user.is_password_reused(form.new_password.data, limit=limit):
            flash(
                f'This password was used recently. '
                f'Please choose a different one (last {limit} passwords cannot be reused).',
                'danger'
            )
            return render_template('reset_password.html', form=form, token=token)
        user.set_password(form.new_password.data)
        tok_record.used = True
        db.session.commit()
        flash('Password updated successfully! You can now sign in.', 'success')
        return redirect(url_for('main.reset_success'))
    if form.errors and request.method == 'POST':
        for field, errs in form.errors.items():
            for err in errs:
                flash(err, 'danger')
    return render_template('reset_password.html', form=form, token=token)
@main.route('/reset-success')
def reset_success():
    return render_template('reset_success.html')

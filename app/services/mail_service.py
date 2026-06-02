from flask import current_app, url_for
from flask_mail import Message
def send_reset_email(user, token: str) -> bool:
    reset_url = url_for('main.reset_password', token=token, _external=True)
    mail_server = current_app.config.get('MAIL_SERVER', 'localhost')
    mail_user   = current_app.config.get('MAIL_USERNAME') or ''
    if mail_server == 'localhost' or not mail_user:
        print(
            f"\n{'='*60}\n"
            f"  [RESET EMAIL] To: {user.email}\n"
            f"  Subject: Reset your FASTag password\n"
            f"  Reset Link: {reset_url}\n"
            f"  (Link expires in 30 minutes)\n"
            f"{'='*60}\n"
        )
        return True
    try:
        from app import mail
        msg = Message(
            subject='Reset your FASTag Portal password',
            recipients=[user.email],
            html=f"""
            <p>Hello {user.full_name},</p>
            <p>You requested a password reset for your FASTag account.</p>
            <p>
              <a href="{reset_url}" style="
                background:#FF6B00;color:#fff;padding:12px 24px;
                border-radius:8px;text-decoration:none;font-weight:600;">
                Reset Password
              </a>
            </p>
            <p>This link expires in <strong>30 minutes</strong>.</p>
            <p>If you did not request this, please ignore this email.</p>
            <br>
            <p style="color:#888;font-size:12px;">
              NHAI FASTag Portal · Powered by NPCI
            </p>
            """,
        )
        mail.send(msg)
        return True
    except Exception as exc:
        current_app.logger.error(f'Reset email send failed: {exc}')
        return False

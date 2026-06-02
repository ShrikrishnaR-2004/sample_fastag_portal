from datetime import datetime, timezone
from flask_login import UserMixin
from . import db, bcrypt
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key=True)
    full_name    = db.Column(db.String(120), nullable=False)
    phone        = db.Column(db.String(15),  nullable=False, unique=True, index=True)
    email        = db.Column(db.String(150), nullable=False, unique=True, index=True)
    dob          = db.Column(db.Date,        nullable=False)
    aadhaar_hash = db.Column(db.String(64), nullable=True)   
    pan_hash     = db.Column(db.String(64),  nullable=True)   
    vehicle_reg   = db.Column(db.String(15), nullable=True)
    vehicle_type  = db.Column(db.String(30), nullable=True)
    permit_rc     = db.Column(db.String(30), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    mpin_hash     = db.Column(db.String(128), nullable=True)
    is_phone_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active         = db.Column(db.Boolean, default=True,  nullable=False)
    created_at        = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at        = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                  onupdate=lambda: datetime.now(timezone.utc))
    password_history = db.relationship('PasswordHistory', backref='user',
                                        lazy='dynamic', cascade='all, delete-orphan')
    reset_tokens     = db.relationship('PasswordResetToken', backref='user',
                                        lazy='dynamic', cascade='all, delete-orphan')
    def set_password(self, raw_password: str) -> None:
        pw_hash = bcrypt.generate_password_hash(raw_password).decode('utf-8')
        self.password_hash = pw_hash
        history_entry = PasswordHistory(password_hash=pw_hash)
        self.password_history.append(history_entry)
    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)
    def is_password_reused(self, raw_password: str, limit: int = 3) -> bool:
        recent = (self.password_history
                  .order_by(PasswordHistory.created_at.desc())
                  .limit(limit)
                  .all())
        return any(bcrypt.check_password_hash(h.password_hash, raw_password) for h in recent)
    def set_mpin(self, raw_mpin: str) -> None:
        self.mpin_hash = bcrypt.generate_password_hash(raw_mpin).decode('utf-8')
    def check_mpin(self, raw_mpin: str) -> bool:
        if not self.mpin_hash:
            return False
        return bcrypt.check_password_hash(self.mpin_hash, raw_mpin)
    def __repr__(self) -> str:
        return f'<User {self.phone}>'
class PasswordHistory(db.Model):
    __tablename__ = 'password_history'
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    def __repr__(self) -> str:
        return f'<PasswordHistory user={self.user_id}>'
class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    token      = db.Column(db.String(64), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used       = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    @property
    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        exp = self.expires_at
        if exp.tzinfo is None:
            from datetime import timezone as tz
            exp = exp.replace(tzinfo=tz.utc)
        return not self.used and exp > now
    def __repr__(self) -> str:
        return f'<PasswordResetToken user={self.user_id} used={self.used}>'

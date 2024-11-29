from . import db, login_manager
from sqlalchemy.orm import mapped_column, Mapped
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int]  = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]]
    avatar: Mapped[Optional[str]]
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def pwd(self):
        return self.password
    
    @pwd.setter
    def pwd(self, password):
        self.password = generate_password_hash(password)
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
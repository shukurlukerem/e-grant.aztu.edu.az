from sqlalchemy.orm import Session
from app.models.userModel import User
from app.api.endpoints.v1.schemas.userSchema import UserProfileUpdate

def get_user_by_fin(db: Session, fin_kod: str):
    return db.query(User).filter(User.fin_kod == fin_kod).first()

def update_user_profile(db: Session, data: UserProfileUpdate, image_bytes: bytes):
    user = get_user_by_fin(db, data.fin_kod)
    if not user:
        return None

    for field, value in data.dict().items():
        setattr(user, field, value)

    user.image = image_bytes
    user.profile_completed = True
    db.commit()
    db.refresh(user)
    return user

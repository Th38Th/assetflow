from app.models import user, asset
from app.db.session import engine, SQLALCHEMY_DATABASE_URL
from app.db.base import Base

user.Base.metadata.create_all(bind=engine)
asset.Base.metadata.create_all(bind=engine)
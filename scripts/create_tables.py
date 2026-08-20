from database import Base, engine
import db_models

Base.metadata.create_all(bind = engine)

print("Database tables created.")
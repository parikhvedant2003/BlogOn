from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# You can use user and password from dot-env files or environment variables
password = "root123!"
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/blog_platform"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
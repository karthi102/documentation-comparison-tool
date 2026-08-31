from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:qwerty@localhost/documentation_comparison"

engine = create_engine(DATABASE_URL)
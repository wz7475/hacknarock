import os

db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@hacknarock_postgres/{db_name}"

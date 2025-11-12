from sqlalchemy import create_engine, MetaData

# Database URL (SQLite)
DATABASE_URL = "sqlite:///./skillstack.db"

# Create engine and metadata
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

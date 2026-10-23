import hashlib
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Local SQLite database file path
DATABASE_URL = "sqlite:///runevault.db"

# Engine setup (check_same_thread=False allows FastAPI to work safely with SQLite)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, default="Submitted")
    complainant = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime)

    audit_logs = relationship("AuditLog", back_populates="ticket")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    action = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime)
    previous_hash = Column(String, nullable=False)
    current_hash = Column(String, nullable=False)

    ticket = relationship("Ticket", back_populates="audit_logs")

# Automatic SHA-256 Hash
@event.listens_for(AuditLog, 'before_insert')
def hash_audit_trail(mapper, connection, target):
    """
    Automatically links the new audit entry to the previous one and computes SHA-256.
    """
    result = connection.execute(
        AuditLog.__table__.select().order_by(AuditLog.id.desc()).limit(1)
    ).fetchone()

    if result is None:
        target.previous_hash = "0" * 64
    else:
        target.previous_hash = result.current_hash

    raw_data = f"{target.ticket_id}{target.action}{target.payload}{target.timestamp}{target.previous_hash}"
    target.current_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

def init_db():
    Base.metadata.create_all(bind=engine)

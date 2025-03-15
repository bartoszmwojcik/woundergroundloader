from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, unique=True)
    
    # Temperature data (°C)
    temp_avg = Column(Float)
    temp_high = Column(Float)
    temp_low = Column(Float)
    
    # Wind chill data (°C)
    windchill_avg = Column(Float)
    windchill_high = Column(Float)
    windchill_low = Column(Float)
    
    # Wind gust data (km/h)
    windgust_avg = Column(Float)
    windgust_high = Column(Float)
    windgust_low = Column(Float)
    
    # Wind speed data (km/h)
    windspeed_avg = Column(Float)
    windspeed_high = Column(Float)
    windspeed_low = Column(Float)
    
    # Wind direction (degrees from 0-360)
    winddir_avg = Column(Float)
    
    # Precipitation (mm)
    precip_rate = Column(Float)
    
    # Pressure (hPa/mb)
    pressure_max = Column(Float)
    pressure_min = Column(Float)
    
    # Station identification
    station_id = Column(String)

    # Calculated wind power (W)
    power = Column(Float)

    def __repr__(self):
        return f"<WeatherData(timestamp={self.timestamp}, temp_avg={self.temp_avg}°C)>"

def init_db():
    """Initialize the database and create tables"""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

def get_session():
    """Get a new database session"""
    Session = init_db()
    return Session()

def save_weather_data(session, data):
    """
    Save weather data to database if it doesn't exist
    """
    existing = session.query(WeatherData).filter_by(
        timestamp=data['timestamp']
    ).first()
    
    if existing is None:
        weather_record = WeatherData(**data)
        session.add(weather_record)
        session.commit()
        return True
    return False 
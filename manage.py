from models import Base
from services.data_access import DataAccessObject
from settings import DATABASE_URL

data_access_object = DataAccessObject(DATABASE_URL)
Base.metadata.create_all(data_access_object.engine)

from sqlalchemy.orm import sessionmaker

from models import Base, engine

Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

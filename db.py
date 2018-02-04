from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 在这里导入所有的可能与定义模型有关的模块，这样他们才会合适地在 metadata 中注册。
    # 否则，将不得不在第一次执行 init_db() 时先导入他们。
    # import models
    Base.metadata.create_all(bind=engine)
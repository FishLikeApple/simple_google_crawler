from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from create_database import KeyWord, Base, Content, db_file_name, create_database

# judge if the db file exists
try:
    with open(db_file_name, 'r'):
        print(db_file_name+' already exists')
except:
    create_database()

engine = create_engine('sqlite:///'+db_file_name+'?check_same_thread=False')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def create_content(title, url, keyword): 

    content = Content(title=title, url=url, keyword=keyword)
    session.add(content)
    session.commit()

def create_keyword(word):

    keyword = KeyWord(word=word)
    session.add(keyword)
    session.commit()

def read_content(keyword_id=None):

    if keyword_id!=None:
        return session.query(Content).filter_by(keyword_id=keyword_id).all()
    return session.query(Content).all()

def read_keyword(word=None):

    if word!=None:
        return session.query(KeyWord).filter_by(word=word).all()
    return session.query(KeyWord).all()

'''
def update(id, new_name):
    # update the name of a stuff

    plan = session.query(Stuff).filter_by(id=id).one()
    plan.name = new_name
    session.add(plan)
    session.commit()

def update_plan(id, new_name):

    plan = session.query(Plan).filter_by(id=id).one()
    plan.name = new_name
    session.add(plan)
    session.commit()
'''

def delete_content(keyword_id):

    no_need_list = session.query(Content).filter_by(keyword_id=keyword_id).all()
    for no_need in no_need_list: 
        session.delete(no_need)
        session.commit()
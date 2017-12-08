 # -*- coding: utf-8 -*-   
''' file write/read/search/
'''
import os
import json
import logging
import logger
import requests
import sqlalchemy

from logger import log_conf
from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask

app = Flask(__name__)
log = log_conf(app.logger,logging.DEBUG)
settings = 'mysql+mysqldb://root:sky@localhost:3306/test'
Base = declarative_base()

class File_map(Base):
    __tablename__ = 'file_map'

    id = Column(Integer,primary_key=True)
    idex = Column(String(64),nullable=False,unique = True)
    name = Column(String(64))
    description = Column(String(128))
    address = Column(String(512),nullable=False)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,self.idex)

class File_type(Base):
    __tablename__ = 'file_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(32),nullable=False,unique=True)
    description = Column(String(128))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,self.name)

class Address_type(Base):
    __tablename__ = 'address_type'

    id = Column(Integer,primary_key=True)
    name = Column(String(32),nullable=False,unique=True)
    description = Column(String(128))
    
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,self.name)
# 构造外键表
class Refer_file_type(Base):
    ''' an file have only one file type, an file type can be belong to may file.
    '''
    __tablename__ = 'refer_file_type'

    id = Column(Integer,primary_key=True)
    file_map_id = Column(Integer,nullable=False,unique=True)
    file_type_id = Column(Integer,nullable=False)
    ForeignKeyConstraint(
            ['file_map_id', 'file_type_id'],
            ['file_map.id', 'file_type.id'],
            onupdate="CASCADE", ondelete="SET NULL"
    )
    def __repr__(self):
        return '%s' % (self.__class__.__name__)

class Refer_address_type(Base):
    ''' one to may, one address type to may file
    '''
    __tablename__ = 'refer_address_type'

    id = Column(Integer,primary_key=True)
    file_map_id = Column(Integer,nullable=False,unique=True)
    address_type_id = Column(Integer,nullable=False)
    ForeignKeyConstraint(
            ['file_map_id', 'address_type_id'],
            ['file_map.id', 'address_type.id'],
            onupdate="CASCADE", ondelete="SET NULL"
    )
    def __repr__(self):
        return '%s' % (self.__class__.__name__)

def db_session_creat(url=None):
    ''' build an session connect to mysql 
    '''     
    
    if url is None or not isinstance(url,str):
        log.warning("no mysql connection link")    
        return -1

    log.debug("connect to database %s",url)
    engine = create_engine(url)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if session is None:
        log.error("session build failt!!")
    else:
        return session

def db_session_destory(session = None):
    if session is not None:
        #log.info("database session was close")
        session.close()
def db_session_commit(session=None):
    try:
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        log.error(e)

class File_db(object):
    """ handle table file_map that reference to file index and address.
    """
    def __init__(self):
        global settings
        self.session = db_session_creat(settings)

    def __del__(self):
        db_session_destory(self.session)
    
    def file_add(self,file_idex = None,fname = None,address = None,fdescription = None,filetype='other',adr_type = 'path'):
        ''' add file index name type to and path to  database
        '''
        log.info('file %s address  %s',file_idex,address)
        if isinstance(file_idex,str) and isinstance(address,str):
            log.debug("session add")
            # file
            new_file = File_map(idex=file_idex,address=address,name=fname,description= fdescription)
            self.session.add(new_file)
            log.debug("id %s",new_file.id)
            db_session_commit(session=self.session)
            log.debug("id %s",new_file.id)
            # file refer 
            if new_file.id is not None:
                log.debug("session  add refer file type")
                new_ref_file = Refer_file_type()
                new_ref_file.file_map_id = new_file.id;
                new_ref_file.file_type_id = self.session.query(File_type).filter(File_type.name == filetype).one().id
                self.session.add(new_ref_file)
                log.debug("session add  refer file type %d",new_ref_file.file_type_id)
                db_session_commit(session=self.session)
                # address refer 
                log.debug("session add  refer address ")
                new_ref_address = Refer_address_type()
                new_ref_address.file_map_id = new_file.id;
                new_ref_address.address_type_id = self.session.query(Address_type).filter(Address_type.name == 'ftp').one().id
                log.debug("address id %d ",new_ref_address.address_type_id)
                self.session.add(new_ref_address)
                db_session_commit(session=self.session)
            else:
                log.warning("failt in adding file %s(%s)",fname,file_idex)
    
    def file_idex_search_key(self,key=None):
        ''' find list by key world
        '''
        keys='%'+key+'%'
        return self.session.query(File_map.idex).filter(File_map.idex.like(keys)).all()
    def file_address_get_by_idex(self,idex=None):
        '''get file location by idex
        '''
        return self.session.query(File_map.address).filter(File_map.idex == idex).one()
#     def get_file_address(String  idex):
#        """ return file path,and it's type
#        """
if __name__ == '__main__':

    log.warning('start to test')
    fdb = File_db()
    log.warning('file add')
    fdb.file_add(file_idex = 'micheal',fname='test',filetype = 'pdf')
    find = fdb.file_idex_search_key(key = 'sky')
    log.debug("find -> %s",find)
    log.debug('find --> %s',find[0][0])
    path = fdb.file_address_get_by_idex(find[0][0])
    log.debug('address = %s',path)

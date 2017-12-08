# -*- coding: utf-8 -*-   
import os
import logging
from flask import Flask

app = Flask(__name__)

def log_conf(logger=None,level=None):
    
    fh = logging.FileHandler('log.txt')  #创建一个文件
    sh = logging.StreamHandler()

    if level is None:
        logger.setLevel(logging.WARNING)  #设置日志记录级别    
        fh.setLevel(logging.INFO)  #设置日志记录级别
        sh.setLevel(logging.WARNING)
    else:
        logger.setLevel(level)  #设置日志记录级别    
        fh.setLevel(level)  #设置日志记录级别
        sh.setLevel(level)
    
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    sh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger


if __name__ == '__main__':
    log = log_conf(app.logger,logging.DEBUG)
    log.critical("软件已废")
    log.error("某些功能不能运行")
    log.warning("有警告")
    log.info("正常")
    log.debug("调试") #忽略
# coding:utf-8
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.path.abspath('.')+r'\upload_file'    # 上传文件的目录


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOEN = True    # 自动提交数据库变动


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
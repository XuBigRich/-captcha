# config/settings.py
import os

class Settings:
    # 图片保存路径
    IMAGE_SAVE_PATH = os.path.join(os.path.dirname(__file__), "../images")
    # 日志配置
    LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs")
    LOG_LEVEL = "DEBUG"
    
settings = Settings()
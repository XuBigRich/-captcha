# main.py
import os
import time
from loguru import logger
from config.settings import settings
from login.Login import Login
from captcha.downloader import CaptchaDownloader
from captcha.recognizer import CaptchaRecognizer
from utils.trajectory import TrajectoryGenerator


def setup_logger():
    """配置日志"""
    os.makedirs(settings.LOG_PATH, exist_ok=True)
    log_file = os.path.join(settings.LOG_PATH, f"captcha_{time.strftime('%Y%m%d')}.log")
    logger.add(log_file, rotation="10 MB", level=settings.LOG_LEVEL)


def main():
    setup_logger()

    # 初始化组件
    downloader = CaptchaDownloader()
    recognizer = CaptchaRecognizer()
    trajectory_gen = TrajectoryGenerator()
    data = downloader.download_from_url("http://localhost:48080/admin-api/system/captcha/get")
    print(data)
    # 示例: 识别本地滑块验证码
    bg_path = data.get("original_image_path")  # 背景图片路径
    target_path = data.get("jigsaw_image_path")  # 滑块图片路径
    token = data.get("token")
    secretKey = data.get("secretKey")
    # 识别缺口位置
    gap_position = recognizer.recognize_slider(target_path, bg_path)
    gap_position=gap_position
    if gap_position is None:
        logger.error("无法识别滑块位置")
        return

    # 生成移动轨迹
    # trajectory = trajectory_gen.generate_trajectory(gap_position)
    # if not trajectory:
    #     logger.error("无法生成移动轨迹")
    #     return
    #
    # logger.info(f"滑块移动轨迹: {trajectory}")

    # 这里可以添加实际的滑动操作代码
    # 例如使用selenium模拟滑动
    login = Login(secretKey,gap_position,token)
    captchaResult = login.check_captcha()
    print(captchaResult)
    loginResult=login.login("教培管理","admin","admin123")
    print(loginResult)
    logger.success("滑块验证码处理完成")


if __name__ == "__main__":
    main()

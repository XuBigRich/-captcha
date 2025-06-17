# captcha/recognizer.py
import ddddocr
import cv2
import numpy as np
from loguru import logger
from PIL import Image
from io import BytesIO


class CaptchaRecognizer:
    def __init__(self):
        self.ocr = ddddocr.DdddOcr(det=False, ocr=False)

    def recognize_slider(self, target_path, bg_path):
        """
        识别滑块验证码
        :param target_path: 滑块图片路径
        :param bg_path: 背景图片路径
        :return: 缺口位置x坐标
        """
        try:
            # 读取图片
            with open(target_path, 'rb') as f:
                target_bytes = f.read()
            with open(bg_path, 'rb') as f:
                bg_bytes = f.read()

            # 识别缺口
            res = self.ocr.slide_match(target_bytes, bg_bytes)
            x_pos = res['target'][0]

            logger.info(f"识别成功，缺口位置: {x_pos}px")
            return x_pos
        except Exception as e:
            logger.error(f"识别滑块失败: {e}")
            return None

    def save_processed_image(self, image, path):
        """保存处理后的图片"""
        try:
            if isinstance(image, np.ndarray):
                image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            image.save(path)
            logger.info(f"图片已保存: {path}")
        except Exception as e:
            logger.error(f"保存图片失败: {e}")
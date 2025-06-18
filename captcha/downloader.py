# captcha/downloader.py
import base64
import os
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from loguru import logger
from config.settings import settings


class CaptchaDownloader:
    def __init__(self):
        os.makedirs(settings.IMAGE_SAVE_PATH, exist_ok=True)

    def download_from_url(self, url):
        """从URL下载验证码图片"""
        try:
            response = requests.post(url, json={"captchaType": "blockPuzzle"})
            response.raise_for_status()
            repData = response.json().get("repData", {})
            originalImageBase64 = repData.get("originalImageBase64")
            jigsawImageBase64 = repData.get("jigsawImageBase64")

            original_save_path = os.path.join(settings.IMAGE_SAVE_PATH, "originalImage.png")
            jigsaw_save_path = os.path.join(settings.IMAGE_SAVE_PATH, "jigsawImage.png")

            # 保存图片
            with open(original_save_path, 'wb') as f:
                f.write(base64.b64decode(originalImageBase64))
            with open(jigsaw_save_path, 'wb') as f:
                f.write(base64.b64decode(jigsawImageBase64))

            logger.success(f"验证码图片已保存到: {original_save_path} 和 {jigsaw_save_path}")
            return {
                "original_image_path": original_save_path,
                "jigsaw_image_path": jigsaw_save_path,
                "token": repData.get("token"),
                "secretKey": repData.get("secretKey")
            }
        except Exception as e:
            logger.error(f"下载验证码失败: {e}")
            return None

    def load_local_image(self, image_path):
        """加载本地验证码图片"""
        if not os.path.exists(image_path):
            logger.error(f"图片不存在: {image_path}")
            return None

        try:
            with Image.open(image_path) as img:
                return img.copy()
        except Exception as e:
            logger.error(f"加载图片失败: {e}")
            return None

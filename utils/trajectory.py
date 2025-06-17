# utils/trajectory.py
import random
import math
from loguru import logger


class TrajectoryGenerator:
    @staticmethod
    def generate_trajectory(distance, duration=2000):
        """
        生成滑块移动轨迹
        :param distance: 需要滑动的总距离(像素)
        :param duration: 滑动总时间(毫秒)
        :return: 轨迹列表 [(x, y, timestamp)]
        """
        try:
            # 轨迹点数量
            point_count = random.randint(5, 8)

            # 生成时间间隔
            time_intervals = [random.randint(100, 300) for _ in range(point_count)]
            total_time = sum(time_intervals)

            # 调整时间间隔使总时间为duration
            ratio = duration / total_time
            time_intervals = [int(t * ratio) for t in time_intervals]

            # 生成距离间隔
            distance_intervals = []
            remaining = distance
            for i in range(point_count - 1):
                max_step = min(remaining, int(distance / (point_count - i) * 1.5))
                step = random.randint(10, max_step)
                distance_intervals.append(step)
                remaining -= step
            distance_intervals.append(remaining)

            # 生成轨迹
            trajectory = []
            current_x = 0
            current_time = 0

            for i in range(point_count):
                current_x += distance_intervals[i]
                current_time += time_intervals[i]
                trajectory.append((current_x, 0, current_time))

                # 添加一些随机抖动
                if i < point_count - 1:
                    jitter_count = random.randint(1, 3)
                    for _ in range(jitter_count):
                        jitter_x = current_x + random.randint(-5, 5)
                        jitter_time = current_time + random.randint(10, 50)
                        trajectory.append((jitter_x, 0, jitter_time))

            logger.info(f"生成轨迹成功，总距离: {distance}px, 总时间: {duration}ms")
            return trajectory
        except Exception as e:
            logger.error(f"生成轨迹失败: {e}")
            return None
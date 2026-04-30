# Copyright (c) 2025, Unitree Robotics Co., Ltd. All Rights Reserved.
# License: Apache License, Version 2.0  
"""
camera state
"""     

from __future__ import annotations

from typing import TYPE_CHECKING
import torch
import sys
import os
import threading
import queue

# add the project root directory to the path, so that the shared memory tool can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tools.shared_memory_utils import MultiImageWriter

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

# create the global multi-image shared memory writer
multi_image_writer = MultiImageWriter()

def set_writer_options(enable_jpeg: bool = False, jpeg_quality: int = 85, skip_cvtcolor: bool = False):
    try:
        multi_image_writer.set_options(enable_jpeg=enable_jpeg, jpeg_quality=jpeg_quality, skip_cvtcolor=skip_cvtcolor)
        print(f"[camera_state] writer options: jpeg={enable_jpeg}, quality={jpeg_quality}, skip_cvtcolor={skip_cvtcolor}")
    except Exception as e:
        print(f"[camera_state] failed to set writer options: {e}")


_camera_cache = {
    'available_cameras': None,
    'camera_keys': None,
    'last_scene_id': None,
    'frame_step': 0,
    'write_interval_steps': 2,
}


_return_placeholder = None
_async_queue = None
_async_thread = None
_async_started = False

def _async_writer_loop(q: "queue.Queue", writer: MultiImageWriter):
    while True:
        try:
            item = q.get()
            if item is None:
                break
            writer.write_images(item)
        except Exception as e:
            print(f"[camera_state] Async writer error: {e}")

def _ensure_async_started():
    global _async_started, _async_queue, _async_thread
    if not _async_started:
        _async_queue = queue.Queue(maxsize=1)
        _async_thread = threading.Thread(target=_async_writer_loop, args=(_async_queue, multi_image_writer), daemon=True)
        _async_thread.start()
        _async_started = True


def get_camera_image(
    env: ManagerBasedRLEnv,
) -> dict:
    # pass
    """get multiple camera images and write them to shared memory
    
    Args:
        env: ManagerBasedRLEnv - reinforcement learning environment instance
    
    Returns:
        dict: dictionary containing multiple camera images
    """

    # ============================================
   # 1. 初始化全局占位符（首次调用时执行）
   # ============================================
    global _return_placeholder
    if _return_placeholder is None:
        _return_placeholder = torch.zeros((1, 480, 640, 3))

   # ============================================
   # 2. 帧步数更新（用于控制处理频率）
   # ============================================
   # 使用模运算循环计数，实现每隔 write_interval_steps 帧处理一次
   # 这是一种降采样机制，避免每帧都进行耗时的图像处理和写入操作
    _camera_cache['frame_step'] = (_camera_cache['frame_step'] + 1) % max(1, _camera_cache['write_interval_steps'])

   #  ============================================
   # 3. 场景变化检测与相机列表缓存
   # ============================================
   # 获取当前场景的内存地址作为唯一标识符
    scene_id = id(env.scene)
    print("This is the information of cameras!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("scene_id",scene_id)
    print("camera keys:",list(env.scene.keys()))


    if _camera_cache['last_scene_id'] != scene_id:
        _camera_cache['camera_keys'] = list(env.scene.keys())
        _camera_cache['available_cameras'] = [name for name in _camera_cache['camera_keys'] if "camera" in name.lower()]
        _camera_cache['last_scene_id'] = scene_id

   # ============================================
   # 4. 传感器更新（仅在特定帧间隔执行）
   # ============================================
   # 当 frame_step 为 0 时（即到达设定的间隔），强制更新传感器状态
    if _camera_cache['frame_step'] == 0:
        try:
            dt = getattr(env, 'physics_dt', 0.02)
            if hasattr(env.scene, 'sensors') and env.scene.sensors:
                for sensor in env.scene.sensors.values():
                    try:
                        sensor.update(dt, force_recompute=False)
                    except Exception:
                        pass
        except Exception:
            pass
    

    # ============================================
   # 5. 图像采集主逻辑
   # ============================================
    # get the camera images
    images = {}
    # env.sim.render()
    

    camera_keys = _camera_cache['camera_keys']
    # Head camera (front camera)
    import cv2
    
    # -------------------------------------
   # 5.1 尝试获取前视相机（head camera）
   # -------------------------------------
    if "front_camera" in camera_keys:
        head_image = env.scene["front_camera"].data.output["rgb"][0]  # [batch, height, width, 3]

        if head_image.device.type == 'cpu':
            images["head"] = head_image.numpy()
            print("dsad")
            
        else:
            images["head"] = head_image.cpu().numpy()
            
    
    # Left camera (left wrist camera)
    # -------------------------------------
   # 5.2 尝试获取左腕相机（left wrist camera）
   # -------------------------------------
    if "left_wrist_camera" in camera_keys:
        left_image = env.scene["left_wrist_camera"].data.output["rgb"][0]
        if left_image.device.type == 'cpu':
            images["left"] = left_image.numpy()
        else:
            images["left"] = left_image.cpu().numpy()
    
    # Right camera (right wrist camera)  
    # -------------------------------------
   # 5.3 尝试获取右腕相机（right wrist camera）
   # -------------------------------------
    if "right_wrist_camera" in camera_keys:
        right_image = env.scene["right_wrist_camera"].data.output["rgb"][0]
        if right_image.device.type == 'cpu':
            images["right"] = right_image.numpy()
        else:
            images["right"] = right_image.cpu().numpy()

    # -------------------------------------
   # 5.4 尝试获取我的相机
   # -------------------------------------
    # if "my_camera1" in camera_keys:
    #     right_image = env.scene["my_camera1"].data.output["rgb"][0]
    #     if right_image.device.type == 'cpu':
    #         images["right"] = right_image.numpy()
    #     else:
    #         images["right"] = right_image.cpu().numpy()
    
    # if no camera with the specified name is found, try other common camera names
    # ============================================
   # 6. 降级策略：使用任意可用相机
   # ============================================
   # 如果未找到标准命名的相机，尝试使用场景中其他可用相机
    if not images:

        available_cameras = _camera_cache['available_cameras']
        if available_cameras:
            print(f"[camera_state] No standard cameras found. Available cameras: {available_cameras}")
            
            # if there are available cameras, use the first three as head, left, right
            for i, camera_name in enumerate(available_cameras[:3]):
                camera_image = env.scene[camera_name].data.output["rgb"][0]
                
               
                if camera_image.device.type == 'cpu':
                    numpy_image = camera_image.numpy()
                else:
                    numpy_image = camera_image.cpu().numpy()
                
                if i == 0:
                    images["head"] = numpy_image
                elif i == 1:
                    images["left"] = numpy_image
                elif i == 2:
                    images["right"] = numpy_image
    

    # ============================================
   # 7. 异步写入共享内存
   # ============================================
   # 仅在满足两个条件时执行：1) 成功采集到图像  2) 到达设定的帧间隔
    if images and _camera_cache['frame_step'] == 0:
        _ensure_async_started()
        try:
            
            if _async_queue.full():
                _async_queue.get_nowait()
            _async_queue.put_nowait(images)
        except Exception:
            pass
    elif not images:
        print("[camera_state] No camera images found in the environment")
    
    # ============================================
   # 8. 返回固定占位符（注意：不是实际的图像数据）
   # ============================================
   # 真正的图像通过 _async_queue 异步传递
   # 这种设计可能是为了与某些固定接口兼容，或避免阻塞主线程
    return _return_placeholder


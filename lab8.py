import cv2
import numpy as np

"""
实验室工作 №8 - 变体4
任务要求：
1. 对图像进行预处理 - 仅显示蓝色通道
2. 使用摄像头追踪打印/显示的标记
3. 检测标记是否在画面的右半部分
"""

def apply_blue_channel(frame):
    """
    变体4的图像处理：仅显示蓝色通道
    将图像的红色和绿色通道设置为0，只保留蓝色通道
    """
    blue_channel = frame.copy()
    blue_channel[:, :, 0] = 0  # 蓝色通道在OpenCV中是第0个通道？需要确认
    blue_channel[:, :, 1] = 0  # 绿色通道设为0
    # 注意：OpenCV中图像是BGR格式，通道顺序是：0=蓝色, 1=绿色, 2=红色
    # 所以只保留蓝色通道 = 保留通道0，其他设为0
    blue_only = frame.copy()
    blue_only[:, :, 1] = 0  # 绿色通道设为0
    blue_only[:, :, 2] = 0  # 红色通道设为0
    return blue_only

def create_red_mask(hsv):
    """
    创建红色掩膜（追踪红色标记，因为标记中有"STOP RED"文字）
    红色在HSV中有两个范围
    """
    # 红色范围1: 0-10
    lower_red1 = np.array([0, 80, 80])
    upper_red1 = np.array([12, 255, 255])
    
    # 红色范围2: 160-180
    lower_red2 = np.array([158, 80, 80])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    return mask

def preprocess_mask(mask):
    """
    对掩膜进行形态学处理，去除噪声
    """
    kernel = np.ones((5, 5), np.uint8)
    print(kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 开运算去除噪点
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 闭运算填充空洞
    return mask

def find_marker_center(mask):
    """
    找到标记的中心点
    返回: (轮廓, 中心点坐标, 面积) 或 (None, None, 0)
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None, 0
    
    # 找到最大的轮廓
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    
    # 面积阈值，过滤小噪声
    if area < 300:
        return None, None, 0
    
    # 计算中心点
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return largest_contour, (cx, cy), area
    
    return largest_contour, None, area

def draw_info(frame, marker_center, width, height):
    """
    在画面上绘制所有信息
    """
    center_x = width // 2
    
    # 1. 绘制左右分割线
    cv2.line(frame, (center_x, 0), (center_x, height), (255, 255, 255), 3)
    cv2.putText(frame, "LEFT", (10, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "RIGHT", (width - 100, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # 2. 显示标题
    cv2.putText(frame, "Variant 4 - Blue Channel + Red Marker Tracking", 
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # 3. 处理标记检测结果
    if marker_center:
        cx, cy = marker_center
        
        # 绘制标记轮廓和中心点
        cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)  # 红色中心点
        cv2.circle(frame, (cx, cy), 15, (0, 0, 255), 2)  # 外圈
        
        # 判断是否在右半部分（核心功能）
        if cx > center_x:
            # 标记在右侧
            status = "MARKER IN RIGHT HALF"
            status_color = (0, 255, 255)  # 黄色
            # 右侧额外提示
            cv2.putText(frame, ">>> RIGHT SIDE <<<", (width - 250, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        else:
            # 标记在左侧
            status = "MARKER IN LEFT HALF"
            status_color = (255, 255, 0)  # 青色
            # 左侧额外提示
            cv2.putText(frame, "<<< LEFT SIDE >>>", (30, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # 显示状态和坐标
        cv2.putText(frame, status, (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, f"Position: ({cx}, {cy})", (10, 160),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    else:
        # 没有检测到标记
        cv2.putText(frame, "NO RED MARKER DETECTED", (10, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Please place the marker in front of camera", 
                   (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # 4. 显示操作提示
    cv2.putText(frame, "Press 'q' to quit | 'b' to toggle blue channel", 
               (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

def main():
    """
    主程序
    """
    print("=" * 50)
    print("实验室工作 №8 - 变体4")
    print("任务：追踪红色标记，检测是否在画面右半部分")
    print("图像处理：仅显示蓝色通道")
    print("=" * 50)
    print("\n使用说明:")
    print("1. 将标记图片显示在手机屏幕上，或打印出来")
    print("2. 将标记放在摄像头前，确保红色部分清晰可见")
    print("3. 移动标记，观察左右判断结果")
    print("4. 按 'b' 键切换蓝色通道效果")
    print("5. 按 'q' 键退出程序")
    print("=" * 50)
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("错误：无法打开摄像头！")
        print("请检查：")
        print("1. 摄像头是否正确连接")
        print("2. 是否有其他程序占用摄像头")
        print("3. 摄像头权限是否已开启")
        return
    
    print("\n摄像头已启动，开始追踪...")
    
    # 状态变量
    show_blue_channel = True  # 是否显示蓝色通道效果
    
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头画面")
            break
        
        # 获取画面尺寸
        height, width = frame.shape[:2]
        
        # ========== 变体4要求1：仅显示蓝色通道 ==========
        if show_blue_channel:
            display_frame = apply_blue_channel(frame)
        else:
            display_frame = frame.copy()
        
        # ========== 变体4要求2：追踪标记 ==========
        # 转换到HSV色彩空间（在原图上进行，因为需要颜色信息）
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 创建红色掩膜
        mask = create_red_mask(hsv)
        mask = preprocess_mask(mask)
        
        # 找到标记中心
        contour, marker_center, area = find_marker_center(mask)
        
        # 如果找到标记，绘制轮廓
        if contour is not None:
            cv2.drawContours(display_frame, [contour], -1, (0, 255, 0), 2)
        
        # ========== 变体4要求3：判断是否在右半部分 ==========
        draw_info(display_frame, marker_center, width, height)
        
        # 显示掩膜（调试用）
        mask_small = cv2.resize(mask, (320, 240))
        cv2.imshow('Detection Mask (Red)', mask_small)
        
        # 显示主画面
        cv2.imshow('Variant 4 - Marker Tracking', display_frame)
        
        # 按键处理
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):  # 退出
            break
        elif key == ord('b'):  # 切换蓝色通道效果
            show_blue_channel = not show_blue_channel
            status = "开启" if show_blue_channel else "关闭"
            print(f"蓝色通道效果: {status}")
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("\n程序已退出")

if __name__ == "__main__":
    main()
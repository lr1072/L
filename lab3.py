import tkinter as tk
from tkinter import messagebox
import random
import string
import math
import time
import base64
import io

class KeyGeneratorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Game Key Generator - Option 4")
        self.window.geometry("750x600")
        self.window.configure(bg="#0a0a1a")
        self.window.resizable(False, False)
        
        # Animation variables
        self.animation_angle = 0
        self.particles = []
        self.is_animating = False
        self.flash_colors = []
        
        # Create embedded images
        self.create_embedded_images()
        self.setup_ui()
        self.start_background_animation()
        self.create_flash_animation()
    
    def create_embedded_images(self):
        """创建内置的图片（避免外部文件依赖）"""
        try:
            # 创建一个简单的8-bit风格图标作为背景
            self.create_background_image()
            
            # 创建游戏图标
            self.create_game_icon()
            
        except Exception as e:
            print(f"Image creation warning: {e}")
            # 如果图片创建失败，程序仍然可以运行
    
    def create_background_image(self):
        """创建一个简单的8-bit风格背景"""
        try:
            # 创建一个简单的彩色渐变作为背景
            width, height = 750, 600
            self.bg_image = tk.PhotoImage(width=width, height=height)
            
            # 创建渐变背景
            for x in range(0, width, 10):
                for y in range(0, height, 10):
                    # 创建科技感的网格背景
                    r = int(10 + (x / width) * 20)
                    g = int(10 + (y / height) * 20)
                    b = int(30 + (x * y) / (width * height) * 40)
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    self.bg_image.put(color, (x, y))
            
        except:
            # 如果创建失败，使用纯色背景
            self.bg_image = None
    
    def create_game_icon(self):
        """创建游戏图标"""
        try:
            # 创建一个简单的密钥图标
            self.icon_image = tk.PhotoImage(width=64, height=64)
            
            # 绘制一个简单的钥匙图标
            for i in range(64):
                for j in range(64):
                    if (i-32)**2 + (j-32)**2 < 400:  # 圆形
                        if 20 < i < 44 and 28 < j < 36:  # 钥匙柄
                            self.icon_image.put('#ffff00', (i, j))
                        elif 44 < i < 54 and 30 < j < 34:  # 钥匙齿
                            self.icon_image.put('#ffaa00', (i, j))
            
        except:
            self.icon_image = None
    
    def create_flash_animation(self):
        """创建闪烁的颜色序列用于动画"""
        self.flash_colors = [
            '#ff0000', '#ff3300', '#ff6600', '#ff9900', '#ffcc00', '#ffff00',
            '#ccff00', '#99ff00', '#66ff00', '#33ff00', '#00ff00', '#00ff33',
            '#00ff66', '#00ff99', '#00ffcc', '#00ffff', '#00ccff', '#0099ff',
            '#0066ff', '#0033ff', '#0000ff', '#3300ff', '#6600ff', '#9900ff',
            '#cc00ff', '#ff00ff', '#ff00cc', '#ff0099', '#ff0066', '#ff0033'
        ]
    
    def play_sound_effect(self, effect_type):
        """使用系统蜂鸣声模拟音效"""
        try:
            import winsound
            if effect_type == "generate":
                winsound.Beep(600, 100)
                winsound.Beep(800, 100)
                winsound.Beep(1000, 200)
            elif effect_type == "success":
                winsound.Beep(1000, 100)
                winsound.Beep(1200, 100)
                winsound.Beep(1500, 150)
                winsound.Beep(1200, 100)
                winsound.Beep(1500, 200)
            elif effect_type == "copy":
                winsound.Beep(1200, 150)
                winsound.Beep(1500, 100)
        except:
            pass
    
    def create_visual_sound_effect(self, effect_type):
        """创建视觉音效（当音频不可用时）"""
        if effect_type == "generate":
            self.flash_element(self.title_label, 3)
        elif effect_type == "success":
            self.flash_element(self.status_label, 5)
        elif effect_type == "copy":
            self.flash_element(self.copy_btn, 2)
    
    def flash_element(self, element, count):
        """闪烁元素创建视觉反馈"""
        original_color = element.cget('fg')
        colors = ['#ffff00', '#ff0000', '#00ff00', '#00ffff']
        
        def flash(i=0):
            if i < count * 2:
                color = colors[(i // 2) % len(colors)] if i % 2 == 0 else original_color
                element.config(fg=color)
                self.window.after(100, lambda: flash(i + 1))
            else:
                element.config(fg=original_color)
        
        flash()
    
    def setup_ui(self):
        # 设置背景
        if hasattr(self, 'bg_image') and self.bg_image:
            self.bg_label = tk.Label(self.window, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 创建标题区域（包含图标）
        self.setup_animated_title()
        
        # 主内容区域
        self.content_frame = tk.Frame(self.window, bg="#151530", bd=3, relief="ridge")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", width=650, height=400)
        
        # 密钥显示区域
        self.setup_key_display()
        
        # 按钮区域
        self.setup_buttons()
        
        # 信息显示区域
        self.setup_info_display()
        
        # 状态栏
        self.setup_status_bar()
        
        # 动画画布
        self.setup_animation_canvas()
    
    def setup_animated_title(self):
        """设置动画标题和图标"""
        title_frame = tk.Frame(self.window, bg="#0a0a1a")
        title_frame.pack(pady=15)
        
        # 添加图标（如果有）
        if hasattr(self, 'icon_image') and self.icon_image:
            icon_label = tk.Label(title_frame, image=self.icon_image, bg="#0a0a1a")
            icon_label.pack(side="left", padx=10)
        
        self.title_label = tk.Label(
            title_frame, 
            text="🔑 ADVANCED KEY GENERATION SYSTEM 🔑", 
            font=("Courier New", 16, "bold"),
            bg="#0a0a1a",
            fg="#00ffff"
        )
        self.title_label.pack(side="left")
        
        # 标题动画
        self.animate_title()
    
    def animate_title(self):
        """标题颜色动画"""
        colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00', '#ff4444', '#4444ff']
        current_color = colors[self.animation_angle % len(colors)]
        
        self.title_label.config(fg=current_color)
        self.animation_angle += 1
        
        self.window.after(2000, self.animate_title)
    
    def setup_key_display(self):
        """设置密钥显示区域"""
        key_display_frame = tk.Frame(self.content_frame, bg="#151530")
        key_display_frame.pack(pady=20)
        
        # 添加密钥图标
        if hasattr(self, 'icon_image') and self.icon_image:
            key_icon_label = tk.Label(key_display_frame, image=self.icon_image, bg="#151530")
            key_icon_label.pack()
        
        key_label = tk.Label(
            key_display_frame,
            text="GENERATED KEY:",
            font=("Arial", 12, "bold"),
            bg="#151530",
            fg="#ffff00"
        )
        key_label.pack(pady=5)
        
        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(
            key_display_frame,
            textvariable=self.key_var,
            font=("Consolas", 18, "bold"),
            width=25,
            justify="center",
            state="readonly",
            bg="#1a1a3a",
            fg="#00ff88",
            bd=4,
            relief="sunken"
        )
        self.key_entry.pack(pady=10)
    
    def setup_buttons(self):
        """设置按钮区域"""
        button_frame = tk.Frame(self.content_frame, bg="#151530")
        button_frame.pack(pady=20)
        
        # Generate button
        self.generate_btn = tk.Button(
            button_frame,
            text="🚀 GENERATE KEY",
            command=self.generate_key_with_animation,
            font=("Arial", 12, "bold"),
            bg="#ff4444",
            fg="white",
            width=16,
            height=2,
            bd=0,
            cursor="hand2",
            activebackground="#ff6666",
            activeforeground="white"
        )
        self.generate_btn.pack(side="left", padx=15)
        
        # Copy button
        self.copy_btn = tk.Button(
            button_frame,
            text="📋 COPY KEY",
            command=self.copy_key_with_animation,
            font=("Arial", 12, "bold"),
            bg="#4444ff",
            fg="white",
            width=16,
            height=2,
            bd=0,
            cursor="hand2",
            activebackground="#6666ff",
            activeforeground="white"
        )
        self.copy_btn.pack(side="left", padx=15)
        
        self.setup_button_hover_effects()
    
    def setup_button_hover_effects(self):
        """设置按钮悬停动画效果"""
        def on_enter_generate(e):
            self.generate_btn.config(bg="#ff6666", fg="#ffff00")
        
        def on_leave_generate(e):
            self.generate_btn.config(bg="#ff4444", fg="white")
        
        def on_enter_copy(e):
            self.copy_btn.config(bg="#6666ff", fg="#ffff00")
        
        def on_leave_copy(e):
            self.copy_btn.config(bg="#4444ff", fg="white")
        
        self.generate_btn.bind("<Enter>", on_enter_generate)
        self.generate_btn.bind("<Leave>", on_leave_generate)
        self.copy_btn.bind("<Enter>", on_enter_copy)
        self.copy_btn.bind("<Leave>", on_leave_copy)
    
    def setup_info_display(self):
        """设置信息显示区域"""
        info_frame = tk.Frame(self.content_frame, bg="#151530")
        info_frame.pack(pady=15, fill="x", padx=20)
        
        info_text = """🎮 TECHNICAL SPECIFICATIONS:

• FORMAT: XXXX-XXXX-XXXX
• EACH BLOCK: 3 LETTERS + 1 DIGIT (RANDOM ORDER)
• WEIGHT SYSTEM: A=1, B=2, ..., Z=26, DIGITS=THEIR VALUE
• TARGET RANGE: EACH BLOCK WEIGHT SUM 30-35
• VALIDATION: AUTOMATIC WEIGHT CALCULATION

✨ EXAMPLE: "AB8U" = A(1) + B(2) + 8(8) + U(21) = 32 ✅"""

        self.info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Courier New", 9),
            bg="#151530",
            fg="#88ff88",
            justify="left"
        )
        self.info_label.pack()
    
    def setup_status_bar(self):
        """设置状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("🎵 SYSTEM READY - CLICK GENERATE TO START 🎵")
        self.status_label = tk.Label(
            self.window,
            textvariable=self.status_var,
            font=("Arial", 10, "bold"),
            bg="#0a0a1a",
            fg="#ffaa00"
        )
        self.status_label.pack(side="bottom", pady=10)
    
    def setup_animation_canvas(self):
        """设置动画画布"""
        self.top_canvas = tk.Canvas(
            self.window,
            width=750,
            height=3,
            bg="#0a0a1a",
            highlightthickness=0
        )
        self.top_canvas.pack(side="top", fill="x")
        
        self.bottom_canvas = tk.Canvas(
            self.window,
            width=750,
            height=3,
            bg="#0a0a1a",
            highlightthickness=0
        )
        self.bottom_canvas.pack(side="bottom", fill="x")
    
    def start_background_animation(self):
        """启动背景动画"""
        self.animate_top_bar()
        self.animate_bottom_bar()
        self.animate_scan_line()
    
    def animate_top_bar(self):
        """顶部条形动画"""
        self.top_canvas.delete("top_bar")
        width = 750
        time_factor = time.time() * 2
        
        for i in range(0, width, 10):
            phase = (i / width + time_factor) % 1.0
            brightness = int(128 + 127 * math.sin(phase * math.pi * 2))
            color = f"#{brightness:02x}{brightness:02x}ff"
            
            self.top_canvas.create_rectangle(
                i, 0, i + 8, 3,
                fill=color, outline="", tags="top_bar"
            )
        
        self.window.after(50, self.animate_top_bar)
    
    def animate_bottom_bar(self):
        """底部条形动画"""
        self.bottom_canvas.delete("bottom_bar")
        width = 750
        time_factor = time.time() * 3
        
        for i in range(0, width, 12):
            phase = (1 - i / width + time_factor) % 1.0
            brightness = int(128 + 127 * math.sin(phase * math.pi * 2))
            color = f"#ff{brightness:02x}{brightness:02x}"
            
            self.bottom_canvas.create_rectangle(
                i, 0, i + 10, 3,
                fill=color, outline="", tags="bottom_bar"
            )
        
        self.window.after(60, self.animate_bottom_bar)
    
    def animate_scan_line(self):
        """扫描线动画"""
        if hasattr(self, 'scan_line_id'):
            self.top_canvas.delete(self.scan_line_id)
        
        x_pos = int((time.time() * 200) % 750)
        self.scan_line_id = self.top_canvas.create_rectangle(
            x_pos - 20, 0, x_pos + 20, 3,
            fill="#ffffff", outline="", stipple="gray50"
        )
        
        self.window.after(100, self.animate_scan_line)
    
    def create_key_generation_animation(self):
        """创建密钥生成动画"""
        self.is_animating = True
        
        def animate_frame(frame=0):
            if self.is_animating:
                loading_texts = [
                    "GENERATING KEY █∙∙∙∙∙",
                    "GENERATING KEY ∙█∙∙∙∙",
                    "GENERATING KEY ∙∙█∙∙∙", 
                    "GENERATING KEY ∙∙∙█∙∙",
                    "GENERATING KEY ∙∙∙∙█∙",
                    "GENERATING KEY ∙∙∙∙∙█"
                ]
                self.status_var.set(loading_texts[frame % len(loading_texts)])
                
                color_index = frame % len(self.flash_colors)
                self.key_entry.config(bg=self.flash_colors[color_index])
                
                self.window.after(150, lambda: animate_frame(frame + 1))
        
        animate_frame()
    
    def generate_particle_effect(self, canvas, x, y, count=10):
        """创建粒子爆发效果"""
        particles = []
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(10, 30)
            size = random.randint(2, 5)
            color = random.choice(['#00ffff', '#ff00ff', '#ffff00', '#00ff00'])
            
            end_x = x + math.cos(angle) * distance
            end_y = y + math.sin(angle) * distance
            
            particle_id = canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=color, outline=""
            )
            particles.append((particle_id, end_x, end_y, size))
        
        def animate_particles(step=0):
            if step < 20:
                for particle_id, end_x, end_y, size in particles:
                    progress = step / 20
                    current_x = x + (end_x - x) * progress
                    current_y = y + (end_y - y) * progress
                    current_size = size * (1 - progress * 0.8)
                    
                    canvas.coords(
                        particle_id,
                        current_x - current_size, current_y - current_size,
                        current_x + current_size, current_y + current_size
                    )
                
                self.window.after(30, lambda: animate_particles(step + 1))
            else:
                for particle_id, _, _, _ in particles:
                    canvas.delete(particle_id)
        
        animate_particles()
    
    def generate_key_with_animation(self):
        """带动画的密钥生成"""
        try:
            self.play_sound_effect("generate")
            self.create_visual_sound_effect("generate")
            
            self.create_key_generation_animation()
            self.status_var.set("🎵 GENERATING KEY WITH 8-BIT MAGIC... 🎵")
            
            self.window.after(2000, self.finish_key_generation)
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Generation failed: {str(e)}")
    
    def finish_key_generation(self):
        """完成密钥生成"""
        try:
            blocks = []
            weights = []
            
            for i in range(3):
                block, weight = self.generate_block()
                blocks.append(block)
                weights.append(weight)
            
            key = "-".join(blocks)
            self.key_var.set(key)
            
            self.is_animating = False
            self.key_entry.config(bg="#1a1a3a")
            
            self.generate_particle_effect(self.top_canvas, 375, 1)
            self.generate_particle_effect(self.bottom_canvas, 375, 1)
            
            weight_info = f"🎉 KEY GENERATED! WEIGHTS: {weights[0]}-{weights[1]}-{weights[2]} 🎉"
            self.status_var.set(weight_info)
            
            self.play_sound_effect("success")
            self.create_visual_sound_effect("success")
            
            print(f"Final Key: {key}")
            print(f"Weight verification: {weights} (Total: {sum(weights)})")
            
        except Exception as e:
            self.is_animating = False
            error_msg = f"❌ GENERATION ERROR: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("SYSTEM ERROR", error_msg)
    
    def copy_key_with_animation(self):
        """带动画的复制功能"""
        key = self.key_var.get()
        if key:
            self.play_sound_effect("copy")
            self.create_visual_sound_effect("copy")
            
            original_bg = self.copy_btn.cget('bg')
            self.copy_btn.config(bg='#00ff00', fg='#000000')
            
            self.window.clipboard_clear()
            self.window.clipboard_append(key)
            self.status_var.set("📋 KEY COPIED TO CLIPBOARD! 📋")
            
            self.generate_particle_effect(self.top_canvas, 650, 1)
            self.generate_particle_effect(self.bottom_canvas, 650, 1)
            
            messagebox.showinfo("SUCCESS", 
                "✅ KEY SUCCESSFULLY COPIED!\n\n"
                "You can now paste it where needed!")
            
            self.window.after(500, lambda: self.copy_btn.config(bg=original_bg, fg='white'))
        else:
            messagebox.showwarning("NOTICE", "⚠️ PLEASE GENERATE A KEY FIRST!")
    
    def get_char_weight(self, char):
        """获取字符权重值"""
        if char.isdigit():
            return int(char)
        elif char.isalpha():
            return ord(char.upper()) - ord('A') + 1
        return 0
    
    def generate_block(self):
        """生成符合权重要求的区块"""
        max_attempts = 500
        
        for _ in range(max_attempts):
            letters = [random.choice(string.ascii_uppercase) for _ in range(3)]
            digit = random.choice(string.digits)
            
            characters = letters + [digit]
            random.shuffle(characters)
            block = ''.join(characters)
            
            total_weight = sum(self.get_char_weight(c) for c in block)
            
            if 30 <= total_weight <= 35:
                return block, total_weight
        
        medium_letters = ['M', 'N', 'O', 'P', 'Q', 'R', 'S']
        digit = random.choice(['5', '6', '7', '8'])
        letters = random.sample(medium_letters, 3)
        characters = letters + [digit]
        random.shuffle(characters)
        block = ''.join(characters)
        total_weight = sum(self.get_char_weight(c) for c in block)
        return block, total_weight
    
    def run(self):
        """运行应用程序"""
        print("=" * 60)
        print("       8-BIT KEY GENERATION SYSTEM - OPTION 4")
        print("       WITH EMBEDDED IMAGES & ANIMATIONS")
        print("=" * 60)
        print("Features: Built-in Images, Particle Effects, Sound Feedback")
        print("No external files required!")
        
        self.window.mainloop()

if __name__ == "__main__":
    app = KeyGeneratorApp()
    app.run()
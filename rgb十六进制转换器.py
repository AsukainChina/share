import tkinter as tk
from tkinter import ttk, messagebox
import traceback


def rgb_to_hex(r, g, b):
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be between 0 and 255")
    return f"#{r:02x}{g:02x}{b:02x}".upper()


class RGBConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB 转换器")
        self.root.geometry("400x450")
        self.rgb_list = []

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建RGB输入框架
        input_frame = ttk.LabelFrame(main_frame, text="RGB 输入 (0-255)", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        # 红色通道
        red_frame = ttk.Frame(input_frame)
        red_frame.pack(fill=tk.X, pady=2)
        ttk.Label(red_frame, text="红色 (R):", width=10).pack(side=tk.LEFT)

        self.red_var = tk.StringVar(value="128")
        self.red_entry = ttk.Entry(red_frame, width=5, textvariable=self.red_var)
        self.red_entry.pack(side=tk.LEFT, padx=5)
        self.red_entry.bind("<FocusOut>", self.validate_entry)
        self.red_entry.bind("<Return>", self.validate_entry)

        self.red_slider = ttk.Scale(red_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                    command=lambda _: self.safe_update_from_slider())
        self.red_slider.set(128)
        self.red_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 绿色通道
        green_frame = ttk.Frame(input_frame)
        green_frame.pack(fill=tk.X, pady=2)
        ttk.Label(green_frame, text="绿色 (G):", width=10).pack(side=tk.LEFT)

        self.green_var = tk.StringVar(value="128")
        self.green_entry = ttk.Entry(green_frame, width=5, textvariable=self.green_var)
        self.green_entry.pack(side=tk.LEFT, padx=5)
        self.green_entry.bind("<FocusOut>", self.validate_entry)
        self.green_entry.bind("<Return>", self.validate_entry)

        self.green_slider = ttk.Scale(green_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                      command=lambda _: self.safe_update_from_slider())
        self.green_slider.set(128)
        self.green_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 蓝色通道
        blue_frame = ttk.Frame(input_frame)
        blue_frame.pack(fill=tk.X, pady=2)
        ttk.Label(blue_frame, text="蓝色 (B):", width=10).pack(side=tk.LEFT)

        self.blue_var = tk.StringVar(value="128")
        self.blue_entry = ttk.Entry(blue_frame, width=5, textvariable=self.blue_var)
        self.blue_entry.pack(side=tk.LEFT, padx=5)
        self.blue_entry.bind("<FocusOut>", self.validate_entry)
        self.blue_entry.bind("<Return>", self.validate_entry)

        self.blue_slider = ttk.Scale(blue_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                     command=lambda _: self.safe_update_from_slider())
        self.blue_slider.set(128)
        self.blue_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 颜色预览
        preview_frame = ttk.LabelFrame(main_frame, text="颜色预览", padding="10")
        preview_frame.pack(fill=tk.X, pady=5)

        self.color_preview = tk.Canvas(preview_frame, width=360, height=50, bg="#808080")
        self.color_preview.pack()

        # 十六进制显示
        hex_frame = ttk.Frame(preview_frame)
        hex_frame.pack(pady=5)
        ttk.Label(hex_frame, text="十六进制:").pack(side=tk.LEFT)
        self.hex_var = tk.StringVar(value="#808080")
        self.hex_label = ttk.Label(hex_frame, textvariable=self.hex_var, font=("Arial", 10, "bold"))
        self.hex_label.pack(side=tk.LEFT, padx=5)

        # 列表操作框架
        list_frame = ttk.LabelFrame(main_frame, text="列表操作", padding="10")
        list_frame.pack(fill=tk.X, pady=5)

        # 翻转列表选项
        self.reverse_var = tk.BooleanVar(value=False)
        reverse_check = ttk.Checkbutton(list_frame, text="输出时翻转列表",
                                        variable=self.reverse_var)
        reverse_check.pack(anchor=tk.W)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # 添加按钮
        ttk.Button(button_frame, text="添加到列表", command=self.add_to_list).pack(side=tk.LEFT, padx=5)

        # 完成按钮
        ttk.Button(button_frame, text="完成并输出", command=self.finish_and_print).pack(side=tk.LEFT, padx=5)

        # 清空按钮
        ttk.Button(button_frame, text="清空列表", command=self.clear_list).pack(side=tk.RIGHT, padx=5)

        # 初始更新
        self.safe_update_color_preview()

    def get_rgb_values(self):
        """获取当前RGB值并转换为整数"""
        try:
            r = int(self.red_var.get())
            g = int(self.green_var.get())
            b = int(self.blue_var.get())
            return r, g, b
        except ValueError:
            return None, None, None

    def safe_update_color_preview(self, event=None):
        """安全更新颜色预览 - 忽略任何错误"""
        try:
            self.update_color_preview(event)
        except Exception:
            pass  # 忽略所有错误

    def update_color_preview(self, event=None):
        """更新颜色预览"""
        r, g, b = self.get_rgb_values()
        if r is not None and g is not None and b is not None:
            try:
                hex_color = rgb_to_hex(r, g, b)
                self.color_preview.config(bg=hex_color)
                self.hex_var.set(hex_color)
            except ValueError:
                # 如果值无效，保持当前预览不变
                pass

    def safe_update_from_slider(self, event=None):
        """安全更新输入框的值 - 忽略任何错误"""
        try:
            self.update_from_slider(event)
        except Exception:
            pass  # 忽略所有错误

    def update_from_slider(self, event=None):
        """滑块更新时调用 - 更新输入框的值（三位数格式）"""
        # 获取滑块值并格式化为三位数
        red_value = int(self.red_slider.get())
        green_value = int(self.green_slider.get())
        blue_value = int(self.blue_slider.get())

        # 格式化为三位数（带前导零）
        self.red_var.set(f"{red_value:03d}")
        self.green_var.set(f"{green_value:03d}")
        self.blue_var.set(f"{blue_value:03d}")

        self.safe_update_color_preview()

    def validate_entry(self, event):
        """验证输入框的值是否有效并格式化为三位数"""
        try:
            # 尝试将输入值转换为整数
            r = int(self.red_var.get())
            g = int(self.green_var.get())
            b = int(self.blue_var.get())

            # 检查范围
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError

            # 更新滑块位置
            self.red_slider.set(r)
            self.green_slider.set(g)
            self.blue_slider.set(b)

            # 格式化为三位数（带前导零）
            self.red_var.set(f"{r:03d}")
            self.green_var.set(f"{g:03d}")
            self.blue_var.set(f"{b:03d}")

            self.safe_update_color_preview()
        except ValueError:
            # 恢复为之前有效的值
            try:
                current_red = int(self.red_slider.get())
                current_green = int(self.green_slider.get())
                current_blue = int(self.blue_slider.get())

                self.red_var.set(f"{current_red:03d}")
                self.green_var.set(f"{current_green:03d}")
                self.blue_var.set(f"{current_blue:03d}")

                messagebox.showerror("输入错误", "请输入0-255之间的整数")
            except Exception:
                pass  # 忽略所有错误

    def add_to_list(self):
        """将当前颜色添加到列表"""
        r, g, b = self.get_rgb_values()
        if r is None or g is None or b is None:
            messagebox.showerror("错误", "请输入有效的RGB值")
            return

        try:
            hex_color = rgb_to_hex(r, g, b)
            self.rgb_list.append(hex_color)

            # 在控制台输出当前添加的颜色和整个列表
            print(f"添加颜色: {hex_color}")
            print("当前列表:", self.rgb_list)
            messagebox.showinfo("添加成功", f"已添加颜色: {hex_color}")
        except ValueError:
            messagebox.showerror("错误", "RGB值必须在0-255之间")

    def clear_list(self):
        """清空颜色列表"""
        self.rgb_list = []
        print("颜色列表已清空")
        messagebox.showinfo("清空列表", "颜色列表已清空")

    def finish_and_print(self):
        """输出最终结果并关闭窗口"""
        if self.rgb_list:
            # 检查是否需要翻转列表
            if self.reverse_var.get():
                reversed_list = self.rgb_list[::-1]
                list_str = "[" + ", ".join(f'"{color}"' for color in reversed_list) + "]"
                print("\n翻转后的颜色列表:")
                print(list_str)

                # 复制到剪贴板
                self.root.clipboard_clear()
                self.root.clipboard_append(list_str)
            else:
                list_str = "[" + ", ".join(f'"{color}"' for color in self.rgb_list) + "]"
                print("\n最终颜色列表:")
                print(list_str)

        else:
            print("颜色列表为空")

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RGBConverterApp(root)
    root.mainloop()
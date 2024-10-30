import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
import hashlib
import platform
import uuid
import os
import subprocess
import threading
import datetime
import re




# 生成 Windows 特定设备指纹
def generate_device_fingerprint():
    system_info = platform.uname()
    mac_address = uuid.getnode()
    username = os.getlogin()
    device_data = f"{system_info.system}-{system_info.node}-{system_info.release}-{mac_address}-{username}"
    return hashlib.sha256(device_data.encode()).hexdigest()

# 居中窗口辅助函数
def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# 处理应用程序关闭
def on_closing():
    welcome_window.quit()
    welcome_window.destroy()

# 返回欢迎窗口
def go_back(current_window):
    current_window.destroy()
    welcome_window.deiconify()  # 再次显示欢迎窗口

def open_registration_window():
    global registration_window, uuid_entry, username_entry, password_entry
    registration_window = ttk.Toplevel()
    registration_window.title("注册")
    center_window(registration_window, 300, 300)
    registration_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Create a frame to center the form
    form_frame = ttk.Frame(registration_window)
    form_frame.pack(expand=True)

    # Define a consistent label width
    label_width = 10

    # UUID Row
    uuid_label = ttk.Label(form_frame, text="UUID:", bootstyle=INFO, width=label_width, anchor="w")
    uuid_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    uuid_entry = ttk.Entry(form_frame)
    uuid_entry.grid(row=0, column=1, padx=5, pady=5)

    # Username Row
    username_label = ttk.Label(form_frame, text="用户名:", bootstyle=INFO, width=label_width, anchor="w")
    username_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    username_entry = ttk.Entry(form_frame)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    # Password Row
    password_label = ttk.Label(form_frame, text="密码:", bootstyle=INFO, width=label_width, anchor="w")
    password_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    password_entry = ttk.Entry(form_frame, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    # Register Button
    register_button = ttk.Button(form_frame, text="注册", command=register, bootstyle=SUCCESS)
    register_button.grid(row=3, column=0, columnspan=2, pady=10)
    registration_window.bind('<Return>', lambda event: register())

    # Go Back Button
    go_back_button = ttk.Button(form_frame, text="返回", command=lambda: go_back(registration_window), bootstyle=SECONDARY)
    go_back_button.grid(row=4, column=0, columnspan=2, pady=10)

    welcome_window.withdraw()  # 隐藏欢迎窗口以进行注册



def open_login_window():
    global login_window, username_entry, password_entry
    login_window = ttk.Toplevel()
    login_window.title("登录")
    center_window(login_window, 300, 300)
    login_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Title Label
    title_label = ttk.Label(login_window, text="EchoMimic 登录", font=("Helvetica", 18, "bold"), bootstyle=INFO)
    title_label.pack(pady=10)

    # Create a frame to center the form
    form_frame = ttk.Frame(login_window)
    form_frame.pack(expand=True)

    # Define a consistent label width
    label_width = 10

    # Username Row
    username_label = ttk.Label(form_frame, text="用户名:", bootstyle=INFO, width=label_width, anchor="w")
    username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    username_entry = ttk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    # Password Row
    password_label = ttk.Label(form_frame, text="密码:", bootstyle=INFO, width=label_width, anchor="w")
    password_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    password_entry = ttk.Entry(form_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Login Button
    login_button = ttk.Button(form_frame, text="登录", command=login, bootstyle=SUCCESS)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)
    login_window.bind('<Return>', lambda event: login())  # 将 Enter 键绑定到登录

    # Go Back Button
    go_back_button = ttk.Button(form_frame, text="返回", command=lambda: go_back(login_window), bootstyle=SECONDARY)
    go_back_button.grid(row=3, column=0, columnspan=2, pady=10)

    welcome_window.withdraw()  # 隐藏欢迎窗口以进行登录


# Updated function to validate the username
def validate_username(username):
    # Ensure username is 3-20 characters long, contains at least one letter, and only includes letters, digits, and underscores
    return re.match("^(?=.*[a-zA-Z])[a-zA-Z0-9_]{3,20}$", username)

# Function to validate the password (remains unchanged)
def validate_password(password):
    return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password)

# Function to handle user registration
def register():
    user_uuid = uuid_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    device_fingerprint = generate_device_fingerprint()

    # Check if any fields are empty
    if not user_uuid or not username or not password:
        messagebox.showwarning("输入错误", "请输入所有字段。")
        return

    # Validate username
    if not validate_username(username):
        messagebox.showwarning("用户名无效", "用户名必须是3到20个字符，至少包含一个字母，只能包含字母、数字和下划线。")
        return

    # Validate password
    if not validate_password(password):
        messagebox.showwarning("密码无效", "密码必须至少8个字符，并包含至少一个大写字母、小写字母、数字和特殊字符。")
        return

    # If validation passes, proceed with registration
    try:
        response = requests.post("https://www.rancilili.com/echomimic_register", json={
            "uuid": user_uuid,
            "username": username,
            "password": password,
            "device_fingerprint": device_fingerprint
        })
        data = response.json()

        if response.status_code == 200 and data.get("status") == "success":
            messagebox.showinfo("注册成功", "UUID 验证成功。您现在可以登录。")
            registration_window.destroy()
            welcome_window.deiconify()
        else:
            messagebox.showerror("注册失败", "无效的 UUID 或订阅问题。")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("错误", f"发生错误: {e}")

def login(event=None):
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    device_fingerprint = generate_device_fingerprint()
    login_success = False  # Flag to check login success

    if not username or not password:
        messagebox.showwarning("输入错误", "请输入所有字段。")
    else:
        try:
            response = requests.post("https://www.rancilili.com/echomimic_login", json={
                "username": username,
                "password": password,
                "device_fingerprint": device_fingerprint
            })
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                expiration_date_str = data.get("expiration_date")
                login_success = True  # Set the flag as True on successful login

                # Parse the expiration date (including optional microseconds if they exist)
                try:
                    expiration_date = datetime.datetime.strptime(expiration_date_str, '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    expiration_date = datetime.datetime.strptime(expiration_date_str, '%Y-%m-%d %H:%M:%S')

                # Get current system time
                current_time = datetime.datetime.now()

                # Calculate time remaining
                time_remaining = expiration_date - current_time

                if time_remaining.total_seconds() > 0:
                    days_remaining = time_remaining.days
                    hours_remaining = time_remaining.seconds // 3600

                    if days_remaining > 0:
                        messagebox.showinfo("登录成功", f"欢迎! 您的订阅将在 {days_remaining} 天后到期。")
                    else:
                        messagebox.showinfo("登录成功", f"欢迎! 您的订阅将在 {hours_remaining} 小时后到期。")
                else:
                    messagebox.showwarning("订阅已到期", "您的订阅已过期，请续订。")
                    login_success = False

            else:
                # Login failed, display an error and stay on the login screen
                messagebox.showerror("登录失败", data.get("message", "登录失败。"))
                username_entry.focus_set()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("错误", f"发生错误: {e}")
            username_entry.focus_set()

        # Only proceed if login was successful
        if login_success:
            open_file_selection_window(expiration_date_str)




# Function to open the file selection window
def open_file_selection_window(expiration_date):
    login_window.withdraw()

    file_window = ttk.Toplevel()
    file_window.title("选择文件")
    center_window(file_window, 400, 400)
    file_window.protocol("WM_DELETE_WINDOW", on_closing)

    expiration_label = ttk.Label(file_window, text=f"订阅到期日期: {expiration_date}", bootstyle=INFO)
    expiration_label.pack(pady=10)

    # Create a Notebook for tabs
    notebook = ttk.Notebook(file_window)
    notebook.pack(expand=True, fill="both", pady=10)

    # Tab 1: Lip Sync
    lip_sync_tab = ttk.Frame(notebook)
    notebook.add(lip_sync_tab, text="口型同步")

    lip_folder_path = tk.StringVar()
    lip_file_path = tk.StringVar()
    result_folder_path = tk.StringVar()

    def check_lip_sync_requirements():
        """Enable the Generate button only if all required paths are set"""
        if lip_folder_path.get() and lip_file_path.get() and result_folder_path.get():
            lip_proceed_button.config(state=NORMAL)
        else:
            lip_proceed_button.config(state=DISABLED)

    def select_lip_folder():
        path = filedialog.askdirectory(title="选择图像文件夹")
        if path:
            lip_folder_path.set(path)
            lip_folder_path_label.config(text=path)
            check_lip_sync_requirements()

    def select_lip_audio_file():
        path = filedialog.askopenfilename(title="选择音频文件", filetypes=[("音频文件", "*.mp3 *.wav *.mp4")])
        if path:
            lip_file_path.set(path)
            lip_file_path_label.config(text=path)
            check_lip_sync_requirements()

    def select_result_folder():
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path:
            result_folder_path.set(path)
            result_folder_path_label.config(text=path)
            check_lip_sync_requirements()

    def lip_sync_proceed():
        result_folder = result_folder_path.get() or os.path.join(lip_folder_path.get(), "output")
        os.makedirs(result_folder, exist_ok=True)

        # Call run_inference in a new thread
        run_inference_in_thread(lip_folder_path.get(), lip_file_path.get(), result_folder)

    # Create a frame for Lip Sync tab form
    lip_form_frame = ttk.Frame(lip_sync_tab)
    lip_form_frame.pack(pady=10)

    # Define a consistent label width
    label_width = 12

    # Lip Sync Tab Form
    lip_folder_label = ttk.Label(lip_form_frame, text="图像文件夹:", bootstyle=INFO, width=label_width, anchor="w")
    lip_folder_label.grid(row=0, column=0, padx=5, pady=5)
    lip_folder_button = ttk.Button(lip_form_frame, text="选择", command=select_lip_folder, bootstyle=PRIMARY)
    lip_folder_button.grid(row=0, column=1, padx=5, pady=5)

    lip_folder_path_label = ttk.Label(lip_form_frame, text="", bootstyle=INFO, wraplength=200, anchor="center")
    lip_folder_path_label.grid(row=1, column=0, columnspan=2, pady=2)

    lip_file_label = ttk.Label(lip_form_frame, text="音频文件:", bootstyle=INFO, width=label_width, anchor="w")
    lip_file_label.grid(row=2, column=0, padx=5, pady=5)
    lip_file_button = ttk.Button(lip_form_frame, text="选择", command=select_lip_audio_file, bootstyle=PRIMARY)
    lip_file_button.grid(row=2, column=1, padx=5, pady=5)

    lip_file_path_label = ttk.Label(lip_form_frame, text="", bootstyle=INFO, wraplength=200, anchor="center")
    lip_file_path_label.grid(row=3, column=0, columnspan=2, pady=2)

    result_folder_label = ttk.Label(lip_form_frame, text="输出文件夹:", bootstyle=INFO, width=label_width, anchor="w")
    result_folder_label.grid(row=4, column=0, padx=5, pady=5)
    result_folder_button = ttk.Button(lip_form_frame, text="选择", command=select_result_folder, bootstyle=PRIMARY)
    result_folder_button.grid(row=4, column=1, padx=5, pady=5)

    result_folder_path_label = ttk.Label(lip_form_frame, text="", bootstyle=INFO, wraplength=200, anchor="center")
    result_folder_path_label.grid(row=5, column=0, columnspan=2, pady=2)

    lip_proceed_button = ttk.Button(lip_form_frame, text="生成", command=lip_sync_proceed, bootstyle=SUCCESS, state=DISABLED)
    lip_proceed_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Tab 2: High Full Video Percentage
    bug_tab = ttk.Frame(notebook)
    notebook.add(bug_tab, text="高完整视频百分比")

    bug_folder_path = tk.StringVar()

    def check_bug_requirements():
        """Enable the Generate button only if the bug folder is selected"""
        if bug_folder_path.get() and result_folder_path.get():
            bug_proceed_button.config(state=NORMAL)
        else:
            bug_proceed_button.config(state=DISABLED)

    def select_bug_folder():
        path = filedialog.askdirectory(title="选择视频文件夹")
        if path:
            bug_folder_path.set(path)
            bug_folder_path_label.config(text=path)
            check_bug_requirements()

    def bug_proceed():
        if not bug_folder_path.get():
            messagebox.showwarning("缺少文件夹", "请选择一个视频文件夹。")
        else:
            result_folder = result_folder_path.get() or os.path.join(bug_folder_path.get(), "output")
            os.makedirs(result_folder, exist_ok=True)
            messagebox.showinfo("成功", f"已选择视频文件夹并设置输出文件夹为：{result_folder}")

    # Bug Tab Form
    bug_form_frame = ttk.Frame(bug_tab)
    bug_form_frame.pack(pady=10)

    bug_folder_label = ttk.Label(bug_form_frame, text="视频文件夹:", bootstyle=INFO, width=label_width, anchor="w")
    bug_folder_label.grid(row=0, column=0, padx=5, pady=5)
    bug_folder_button = ttk.Button(bug_form_frame, text="选择", command=select_bug_folder, bootstyle=PRIMARY)
    bug_folder_button.grid(row=0, column=1, padx=5, pady=5)

    bug_folder_path_label = ttk.Label(bug_form_frame, text="", bootstyle=INFO, wraplength=200, anchor="center")
    bug_folder_path_label.grid(row=1, column=0, columnspan=2, pady=2)

    bug_result_folder_label = ttk.Label(bug_form_frame, text="输出文件夹:", bootstyle=INFO, width=label_width, anchor="w")
    bug_result_folder_label.grid(row=2, column=0, padx=5, pady=5)
    bug_result_folder_button = ttk.Button(bug_form_frame, text="选择", command=select_result_folder, bootstyle=PRIMARY)
    bug_result_folder_button.grid(row=2, column=1, padx=5, pady=5)

    bug_result_folder_path_label = ttk.Label(bug_form_frame, text="", bootstyle=INFO, wraplength=200, anchor="center")
    bug_result_folder_path_label.grid(row=3, column=0, columnspan=2, pady=2)

    bug_proceed_button = ttk.Button(bug_form_frame, text="生成", command=bug_proceed, bootstyle=SUCCESS, state=DISABLED)
    bug_proceed_button.grid(row=4, column=0, columnspan=2, pady=20)

    bug_tab.bind('<Return>', lambda event: bug_proceed())
    
# Function to run inference in a separate thread
def run_inference_in_thread(source_path, audio_file, result_path):
    def run():
        try:
            # Replace this with the actual run_inference function
            run_inference(source_path, audio_file, result_path)
            messagebox.showinfo("完成", "所有图像已处理完成！")
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中出错: {e}")
    
    thread = threading.Thread(target=run)
    thread.start()

# Run inference function (with GPU default)
def run_inference(source_path, audio_file, result_path):
    # Set base directory to the current working directory assuming it points to EchoMimic
    base_dir = os.getcwd()
    inference_script_path = os.path.join(base_dir, 'inference.py')
    venv_python_path = os.path.join(base_dir, 'myenv', 'Scripts', 'python.exe')
    checkpoint_dir = os.path.join(base_dir, 'checkpoints')

    # Debug: Print paths and device info
    print("Python Interpreter Path:", venv_python_path)
    print("Inference Script Path:", inference_script_path)
    print("Checkpoint Directory:", checkpoint_dir)

    # Find .jpg files in the source directory
    jpg_files = [f for f in os.listdir(source_path) if f.endswith('.jpg')]

    # Ensure at least one .jpg file and audio file exists
    if not jpg_files:
        raise FileNotFoundError("源目录中未找到 .jpg 文件。")
    if not audio_file or not os.path.isfile(audio_file):
        raise FileNotFoundError("提供的音频文件无效或不存在。")

    # Process each .jpg file one by one using GPU if available
    for jpg_file in jpg_files:
        source_image = os.path.join(source_path, jpg_file)

        # Build command with all flags (excluding --cpu to default to GPU)
        command = [
            venv_python_path, inference_script_path,
            '--driven_audio', audio_file,
            '--source_image', source_image,
            '--result_dir', result_path,
            '--checkpoint_dir', checkpoint_dir,
            '--pose_style', '0',               # Example flag from namespace
            '--batch_size', '1',               # Example flag from namespace
            '--size', '256',                   # Image size
            '--expression_scale', '1.0',       # Expression intensity scaling
            '--still',                         # Treat input as a still image
            '--preprocess', 'full',            # Preprocessing mode
            '--net_recon', 'resnet50',         # Neural net architecture
            '--bfm_folder', './checkpoints/BFM_Fitting/',  # Folder for BFM model
            '--bfm_model', 'BFM_model_front.mat',          # BFM model used
            '--focal', '1015.0',               # Camera focal length
            '--center', '112.0',               # Center for reconstruction
            '--camera_d', '10.0',              # Distance to camera
            '--z_near', '5.0',                 # Near clipping plane
            '--z_far', '15.0',                 # Far clipping plane
        ]

        # Debug: Print the command and device being used
        print("Running command:", " ".join(command))

        try:
            subprocess.run(command, check=True)
            print(f"Completed processing {jpg_file}")
        except Exception as exc:
            print(f"{jpg_file} generated an exception: {exc}")

            
# 欢迎窗口，选择登录或注册
welcome_window = tk.Tk()
welcome_window.title("EchoMimic")

welcome_window.title("欢迎来到 EchoMimic")
center_window(welcome_window, 300, 200)
welcome_window.protocol("WM_DELETE_WINDOW", on_closing)

welcome_label = ttk.Label(welcome_window, text="欢迎来到 EchoMimic", font=("Helvetica", 18, "bold"), bootstyle=INFO)
welcome_label.pack(pady=20)

login_button = ttk.Button(welcome_window, text="登录", command=open_login_window, bootstyle=SUCCESS)
login_button.pack(pady=10)

register_button = ttk.Button(welcome_window, text="注册", command=open_registration_window, bootstyle=PRIMARY)
register_button.pack(pady=10)

# 运行应用程序
welcome_window.mainloop()

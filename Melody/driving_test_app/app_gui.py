"""
Driving Test Slot Monitor - Tkinter GUI
A native desktop GUI to monitor MyRTA driving test slot availability.
使用 tkinter 的原生桌面界面
"""
import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from monitor_core import DrivingTestMonitor


class DrivingTestMonitorGUI:
    """GUI application for driving test monitoring."""

    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Driving Test Monitor / 驾考监控器")
        self.root.geometry("900x700")

        # Set minimum size
        self.root.minsize(800, 600)

        # Monitor instance
        self.monitor = None
        self.monitor_thread = None

        # Create GUI
        self.create_widgets()

        # Center window
        self.center_window()

    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create all GUI widgets."""

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="🚗 Driving Test Slot Monitor / 驾考时间段监控器",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Create notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Tab 1: Booking Information
        booking_frame = ttk.Frame(notebook, padding="10")
        notebook.add(booking_frame, text="📋 Booking Info / 预订信息")
        self.create_booking_tab(booking_frame)

        # Tab 2: Notification Settings
        notification_frame = ttk.Frame(notebook, padding="10")
        notebook.add(notification_frame, text="🔔 Notifications / 通知")
        self.create_notification_tab(notification_frame)

        # Logs section
        logs_frame = ttk.LabelFrame(main_frame, text="📝 Logs / 日志", padding="10")
        logs_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)

        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Courier", 10)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.log_text.config(state=tk.DISABLED)

        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, pady=(0, 5))

        self.start_button = ttk.Button(
            control_frame,
            text="🚀 Start Monitoring / 开始监控",
            command=self.start_monitoring,
            width=30
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(
            control_frame,
            text="⏹ Stop Monitoring / 停止监控",
            command=self.stop_monitoring,
            width=30,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready to start / 准备就绪")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E))

    def create_booking_tab(self, parent):
        """Create booking information tab."""
        # Create form
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.BOTH, expand=True)

        row = 0

        # Booking ID
        ttk.Label(form_frame, text="Booking ID / 预订号:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.booking_id_var = tk.StringVar(value="2931865745")
        ttk.Entry(form_frame, textvariable=self.booking_id_var, width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        # Family Name
        ttk.Label(form_frame, text="Family Name / 姓氏:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.family_name_var = tk.StringVar(value="Qi")
        ttk.Entry(form_frame, textvariable=self.family_name_var, width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        # Preferred Date
        ttk.Label(form_frame, text="Preferred Date / 首选日期 (DD/MM/YYYY):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.preferred_date_var = tk.StringVar(value="27/10/2025")
        ttk.Entry(form_frame, textvariable=self.preferred_date_var, width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        # Suburb
        ttk.Label(form_frame, text="Suburb (lowercase) / 城市（小写）:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.suburb_var = tk.StringVar(value="rockdale")
        ttk.Entry(form_frame, textvariable=self.suburb_var, width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        # Suburb Option
        ttk.Label(form_frame, text="Suburb Dropdown Option / 下拉选项:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.suburb_option_var = tk.StringVar(value="ROCKDALE")
        ttk.Entry(form_frame, textvariable=self.suburb_option_var, width=40).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        ttk.Label(form_frame, text="(Usually uppercase / 通常大写)", font=("Arial", 9)).grid(row=row, column=2, sticky=tk.W, pady=5)
        row += 1

        # Check Interval
        ttk.Label(form_frame, text="Check Interval / 检查间隔 (seconds):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.check_interval_var = tk.IntVar(value=5)
        interval_spinbox = ttk.Spinbox(
            form_frame,
            from_=3,
            to=60,
            textvariable=self.check_interval_var,
            width=38
        )
        interval_spinbox.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        row += 1

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def create_notification_tab(self, parent):
        """Create notification settings tab."""
        # Info text
        info_text = """
Pushover 通知设置（可选）/ Pushover Notification Settings (Optional)

如果您想在手机上收到通知，请填写以下信息。
不填写也可以正常使用，找到时间段时浏览器会保持打开。

If you want notifications on your phone, fill in the information below.
The monitor works fine without it - browser stays open when slots are found.

如何获取 / How to get:
1. 访问 pushover.net 注册账号 / Visit pushover.net and sign up
2. 下载手机 APP / Download mobile app
3. 获取 User Key 和 API Token / Get User Key and API Token
        """

        info_label = ttk.Label(parent, text=info_text, justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=(0, 20))

        # Form
        form_frame = ttk.Frame(parent)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Pushover User Key
        ttk.Label(form_frame, text="Pushover User Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.pushover_user_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pushover_user_var, width=50, show="*").grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        # Pushover API Token
        ttk.Label(form_frame, text="Pushover API Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pushover_token_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.pushover_token_var, width=50, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        # Configure column weights
        form_frame.columnconfigure(1, weight=1)

    def log(self, message):
        """Add message to log display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"

        # Update log text in GUI thread
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, full_message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_status(self, status):
        """Update status bar."""
        self.status_var.set(status)

    def validate_inputs(self):
        """Validate user inputs."""
        if not self.booking_id_var.get().strip():
            messagebox.showerror("Error / 错误", "Booking ID is required! / 预订号必填！")
            return False

        if not self.family_name_var.get().strip():
            messagebox.showerror("Error / 错误", "Family Name is required! / 姓氏必填！")
            return False

        if not self.preferred_date_var.get().strip():
            messagebox.showerror("Error / 错误", "Preferred Date is required! / 首选日期必填！")
            return False

        if not self.suburb_var.get().strip():
            messagebox.showerror("Error / 错误", "Suburb is required! / 城市必填！")
            return False

        if not self.suburb_option_var.get().strip():
            messagebox.showerror("Error / 错误", "Suburb Dropdown Option is required! / 下拉选项必填！")
            return False

        return True

    def run_monitor_async(self):
        """Run the monitor in an asyncio event loop."""
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Create monitor instance
            self.monitor = DrivingTestMonitor(
                booking_id=self.booking_id_var.get().strip(),
                family_name=self.family_name_var.get().strip(),
                preferred_date=self.preferred_date_var.get().strip(),
                suburb=self.suburb_var.get().strip(),
                suburb_dropdown_option=self.suburb_option_var.get().strip(),
                check_interval=self.check_interval_var.get(),
                pushover_user=self.pushover_user_var.get().strip() if self.pushover_user_var.get().strip() else None,
                pushover_token=self.pushover_token_var.get().strip() if self.pushover_token_var.get().strip() else None,
                log_callback=lambda msg: self.root.after(0, self.log, msg),
            )

            # Run the monitor
            loop.run_until_complete(self.monitor.start())
        except Exception as e:
            self.root.after(0, self.log, f"❌ Error: {e}")
        finally:
            loop.close()
            # Re-enable start button
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.update_status("Monitoring stopped / 监控已停止"))

    def start_monitoring(self):
        """Start the monitoring process."""
        # Validate inputs
        if not self.validate_inputs():
            return

        # Check if already running
        if self.monitor and self.monitor.is_running():
            messagebox.showwarning("Warning / 警告", "Monitor is already running! / 监控已在运行！")
            return

        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_status("Monitoring started / 监控已开始")

        self.log("=" * 60)
        self.log("Starting Driving Test Slot Monitor / 开始驾考时间段监控")
        self.log("=" * 60)

        # Start monitor in separate thread
        self.monitor_thread = threading.Thread(
            target=self.run_monitor_async,
            daemon=True
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Stop the monitoring process."""
        if self.monitor and self.monitor.is_running():
            self.monitor.stop()
            self.log("Stop signal sent... / 停止信号已发送...")
            self.update_status("Stopping... / 停止中...")
        else:
            messagebox.showinfo("Info / 信息", "Monitor is not running. / 监控未在运行。")

    def on_closing(self):
        """Handle window close event."""
        if self.monitor and self.monitor.is_running():
            if messagebox.askokcancel(
                "Quit / 退出",
                "Monitor is still running. Stop and quit? / 监控仍在运行。停止并退出？"
            ):
                self.monitor.stop()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = DrivingTestMonitorGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

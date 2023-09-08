import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 初期PIDパラメータの設定
Kp = 1.0
Ki = 1.0
Kd = 1.0

# シミュレーション用時間設定
time = np.linspace(0, 10, 1000)

# 制御対象のシステムモデル（二次遅れ系）
omega_n = 2.0  # 自然角周波数
zeta = 1.5     # 減衰比（1より大きい）
system = ctrl.TransferFunction([omega_n**2], [1, 2*zeta*omega_n, omega_n**2])

# グラフデータの初期化
input_signal = np.ones_like(time)
response = np.zeros_like(time)

# パラメータ変更時のコールバック関数
def parameter_changed(event):
    global Kp, Ki, Kd, input_signal, response

    # パラメータを更新
    Kp = Kp_scale.get()
    Ki = Ki_scale.get()
    Kd = Kd_scale.get()

    # 制御器を再構築
    controller = ctrl.TransferFunction([Kd, Ki, Kp], [1, 0])
    closed_loop_system = ctrl.feedback(controller * system, 1)

    # 制御系の応答を計算
    _, response = ctrl.step_response(closed_loop_system, time)

    # グラフを更新
    update_graph()

# グラフを更新する関数
def update_graph():
    ax.clear()
    ax.plot(time, input_signal, label="目標値")
    ax.plot(time, response, label="応答")
    ax.set_xlabel("時間")
    ax.set_ylabel("値")
    ax.legend()
    ax.grid(True)
    canvas.draw()

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("PID Control (Second-Order System)")

# PIDパラメータ入力フレーム
pid_frame = ttk.LabelFrame(root, text="PIDパラメータ")
pid_frame.grid(row=0, column=0, padx=10, pady=10)

Kp_label = ttk.Label(pid_frame, text="Kp:")
Kp_label.grid(row=0, column=0, padx=5, pady=5)
Kp_scale = tk.Scale(pid_frame, from_=0.0, to=10.0, resolution=0.01, orient="horizontal")
Kp_scale.grid(row=0, column=1, padx=5, pady=5)
Kp_scale.set(Kp)
Kp_scale.bind("<Motion>", parameter_changed)  # スライダーが動くたびにパラメータを更新

Ki_label = ttk.Label(pid_frame, text="Ki:")
Ki_label.grid(row=1, column=0, padx=5, pady=5)
Ki_scale = tk.Scale(pid_frame, from_=0.0, to=10.0, resolution=0.01, orient="horizontal")
Ki_scale.grid(row=1, column=1, padx=5, pady=5)
Ki_scale.set(Ki)
Ki_scale.bind("<Motion>", parameter_changed)  # スライダーが動くたびにパラメータを更新

Kd_label = ttk.Label(pid_frame, text="Kd:")
Kd_label.grid(row=2, column=0, padx=5, pady=5)
Kd_scale = tk.Scale(pid_frame, from_=0.0, to=10.0, resolution=0.01, orient="horizontal")
Kd_scale.grid(row=2, column=1, padx=5, pady=5)
Kd_scale.set(Kd)
Kd_scale.bind("<Motion>", parameter_changed)  # スライダーが動くたびにパラメータを更新

# グラフの初期化
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
update_graph()

root.mainloop()

import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk

# PIDパラメータの初期値
Kp = 1.0
Ki = 1.0
Kd = 1.0

# PIDパラメータを設定する関数
def set_pid_parameters():
    global Kp, Ki, Kd
    Kp = float(Kp_entry.get())
    Ki = float(Ki_entry.get())
    Kd = float(Kd_entry.get())

# シミュレーションを実行する関数
def simulate():
    set_pid_parameters()

    # シミュレーション時間
    time = np.linspace(0, 10, 1000)

    # 制御対象のシステムモデル（二次遅れ系）
    omega_n = 2.0      # 自然角周波数
    zeta = 1.5         # 減衰比（1より大きい）
    system = ctrl.TransferFunction([omega_n**2], [1, 2*zeta*omega_n, omega_n**2])

    # PID制御器
    controller = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])

    # 制御系を組み立て
    closed_loop_system = ctrl.feedback(controller * system, 1)

    # ステップ入力信号
    input_signal = np.ones_like(time)

    # 制御系の応答を計算
    time, response = ctrl.step_response(closed_loop_system, time)

    # プロット
    plt.figure()
    plt.plot(time, input_signal, label="目標値")
    plt.plot(time, response, label="応答")
    plt.xlabel("時間")
    plt.ylabel("値")
    plt.legend()
    plt.grid(True)
    plt.show()

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("PID Control (Second-Order System)")

# PIDパラメータ入力フレーム
pid_frame = ttk.LabelFrame(root, text="PIDパラメータ")
pid_frame.grid(row=0, column=0, padx=10, pady=10)

Kp_label = ttk.Label(pid_frame, text="Kp:")
Kp_label.grid(row=0, column=0, padx=5, pady=5)
Kp_entry = ttk.Entry(pid_frame)
Kp_entry.grid(row=0, column=1, padx=5, pady=5)
Kp_entry.insert(0, str(Kp))

Ki_label = ttk.Label(pid_frame, text="Ki:")
Ki_label.grid(row=1, column=0, padx=5, pady=5)
Ki_entry = ttk.Entry(pid_frame)
Ki_entry.grid(row=1, column=1, padx=5, pady=5)
Ki_entry.insert(0, str(Ki))

Kd_label = ttk.Label(pid_frame, text="Kd:")
Kd_label.grid(row=2, column=0, padx=5, pady=5)
Kd_entry = ttk.Entry(pid_frame)
Kd_entry.grid(row=2, column=1, padx=5, pady=5)
Kd_entry.insert(0, str(Kd))

update_button = ttk.Button(pid_frame, text="パラメータ更新", command=set_pid_parameters)
update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# シミュレーションボタン
simulate_button = ttk.Button(root, text="シミュレーション実行", command=simulate)
simulate_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import math

# 目的関数の設定
def custom_func(x0, x1, k):
    result = 1 - np.exp((-((x0 - 250 - 125 * np.sin(Alpha * k))**2) / (2 * 40**2))
             -(((x1 - 250 - 125 * np.cos(Alpha * k))**2) / (2 * 40**2)))
    return result

#３Dグラフの定義
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('x_0')
ax.set_xlabel('x_1')
ax.set_xlabel('z')
x_0 = np.arange(0, 500)
x_1 = np.arange(0, 500)
X, Y = np.meshgrid(x_0, x_1)
 
# 初期設定
N = 100 # 働き蜂と傍観蜂の個体数
d = 2 # 次元
s = np.zeros(N) #更新カウント
lim = 30
xmax  = 500
xmin =0
G = 700 # 繰り返す回数
Alpha = 0.01 #目的関数の変化を制御するパラメータ

 
x_best = [0,0] #x_bestの初期化

x = np.zeros((N,d)) #蜂の配置
for i in range(N):
    x[i] = (xmax-xmin)*np.random.rand(d) + xmin
 
def fit(x0, x1, i): #新しい餌場候補の適合度
    z = custom_func(x0, x1, i)
    if z > 0:
        return 1/(1+z)
    else: return 1+abs(z)
 
# ルーレット選択用関数
def roulette_choice(w):
    tot = []
    acc = 0
    for e in w:
        acc += e
        tot.append(acc)
 
    r = np.random.random() * acc
    for i, e in enumerate(tot):
        if r <= e:
            return i

 
# 繰り返し
best_value = []
x_best_value = [0, 0]
ims = []
for g in range(G):
    # 働き蜂employee bee step
    for i in range(N):
        v = x.copy()
        k = i
        while k == i:
            k = np.random.randint(N)
        j = np.random.randint(d)
        r = np.random.rand()*2 - 1 # -1から1までの一様乱数
        v[i,j] = x[i,j] + r * (x[i,j] - x[k,j])
 
        if fit(*x[i], g) < fit(*v[i], g): #適合度に基づいて働き蜂の情報を更新
            x[i] = v[i]
        if fit(*x[i], g) <= fit(*v[i], g):
            s[i] = 0
        else: s[i] += 1
 
    # 傍観蜂onlooker bee step
    w = []
    for i in range(N):
        w.append(fit(*x[i], g))
    
    for l in range(N):
        i = roulette_choice(w)
        j = np.random.randint(d)
        r = np.random.rand()*2 - 1 # -1から1までの一様乱数
        v[i,j] = x[i,j] + r * (x[i,j] - x[k,j])
        if fit(*x[i], g) < fit(*v[i], g):
            x[i] = v[i]
        if fit(*x[i], g) <= fit(*v[i], g):
            s[i] = 0
        else: s[i] += 1
 
 
    # 斥候蜂scout bee step
    for i in range(N):
        if s[i] >= lim:
            for j in range(d):
                x[i,j] = np.random.rand()*(xmax-xmin) + xmin
            s[i] = 0
 
    # 最良個体の発見
    z = np.zeros(N)
    best = float('-inf')  # 初期値をマイナス無限大に設定
    for i in range(N):
    #    if best > custom_func(*x[i], g): #時変関数に対応させるために削除
        z[i] = fit(*x[i], g)
        if z[i] > best:
            best = max(z)
            x_best = x[i].copy()
    
    best_value.append(custom_func(*x_best, g))
    x_best_value.append(x_best)
    print("発見した最小値：{}\nそのときのx：{}".format(custom_func(*x_best, g), x_best))

    #アニメーションの座標保存
    im = ax.scatter3D(*x_best, custom_func(*x_best, g), c='r', s=0.5, alpha=0.5)
    ims.append(im)

 
# 結果の表示
# 3D平面上で最適解の座標をプロット
ax.plot_wireframe(X, Y, custom_func(X, Y, g), color='b', linewidth=0.3, alpha=0.3)   
ani = animation.ArtistAnimation(fig, ims)
plt.show()
#ani.save('./3D-animation.gif', writer='pillow')
#plt.close()

plt.plot(range(G), best_value)
plt.yscale('log')
plt.title("Time-varying funktion")
plt.xlabel("試行回数")
plt.ylabel("発見した最小値")
plt.show()

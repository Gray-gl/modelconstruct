# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

flag=0
# 读取体素模型的文件
def read(path):
    result = []
    with open(path, 'r') as f:
        for line in f.readlines():
            temp = []
            for a in line.strip().split(','):
                temp.append(float(a))
            result.append(temp)
    # result是[[x,y,z,0],[x1,y1,z1,1],....]的形式，你可以直接读取
    return result

def layer_sizes():
    #这你妈的没用上？
    n_x = 3  #x,y,z
    n_h = 81 #定义隐藏层size
    n_y = 4  #a,b,c,d


def initialize_parameters(X, n_x, n_h, n_y):
    #初始化平面
    W = []
    w_x = 0
    w_y = 0
    w_z = 0
    for i in range(len(X)):
        w_x += X[i][0]
        w_y += X[i][1]
        w_z += X[i][2]
    w_x /= len(X)
    w_y /= len(X)
    w_z /= len(X)
    #到这里为止求出了重心坐标，然后要生成27个不同的平面放入minout里面
    # TODO 那么由内向外的法向量是abc,如果数据集中心为0点
    a = w_x - 0
    b = w_y - 0
    c = w_z - 0
    print(a,b,c)
    new_a = a / math.sqrt(a * a + b * b + c * c)
    new_b = b / math.sqrt(a * a + b * b + c * c)
    new_c = c / math.sqrt(a * a + b * b + c * c)
    print([new_a,new_b,new_c])
    # TODO 计算出球面上的xyz，我们假定外接球半径为2
    x = 2 * new_a
    y = 2 * new_b
    z = 2 * new_c
    r = math.sqrt(x * x + y * y + z * z)
    theta = math.acos(z / r)
    varphi = math.atan(y / x)
    #TODO 这里其实就要开始入手了
    for i in range(3):
        # TODO 高斯分布
        # TODO 高斯分布的扰动应该在球面坐标上扰动
        #delta_r = random.gauss(0, 5e-2)
        delta_theta = random.gauss(0,5e-2) * math.pi
        delta_varphi = random.gauss(0,5e-2) * math.pi * 2
        #这也不用归一化，真的方便
        r = r
        theta = theta + delta_theta
        varphi = varphi + delta_varphi
        W.append([r,theta,varphi])
    #不带高斯扰动的生成24个平面
    for i in range(24):
        r = 2
        theta = random.random() * math.pi
        varphi = random.random() * 2 * math.pi
        W.append([r,theta,varphi])
    #通过初始化的球面坐标生成平面坐标，这样就不会影响前向传播的结果？
    W1 = []
    b1 = []
    for i in range(W.__len__()):
        r = W[i][0]
        theta = W[i][1]
        varphi = W[i][2]
        x = r * math.sin(theta) * math.cos(varphi)
        y = r * math.sin(theta) * math.sin(varphi)
        z = r * math.cos(theta)
        A = 0 - x
        B = 0 - y
        C = 0 - z
        D = -1 * x * A - y * B - z * C
        W1.append([A,B,C])
        b1.append([D])
    W1 = np.array(W1)
    b1 = np.array(b1)
    W = np.array(W)
    # print(W1)
    # print(b1)
    parameters = {"W1": W1, "b1": b1, "W": W}
    return parameters

#Z1其实是Ax+By+Cz+D的结果
#TODO 这里要把球面坐标转换为平面坐标吗,别忘记现在中心点为0
def forward_propagation(X, parameters):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    xyz=X[:,:3]
    Z1 = np.dot(xyz,W1.T) + b1.T  #Z1=AX+BY+CZ+D 返回(3万,3)*(3,16)+(1,16)=(3万，16)
    return Z1

#计算loss函数的部分
def compute_cost(Z1,n_h,parameters):
    minout=np.zeros(n_h)
    for i in range(n_h):
        a,b,c=parameters["W1"][i]
        d=parameters["b1"][i]
        deno=math.sqrt(a*a+b*b+c*c)
        for j in range(len(Z1)):
            #TODO 正半轴loss需要考量，按理来说正半轴的loss一定和距离有关，且不能大于一次方
            #所以loss = r的收敛属于特殊情况？
            R = Z1[j][i] / deno
            if(R>=0):
                # minout[i] += (1-math.e**(-1*Z1[j][i]/deno)) * 10
                # minout[i] += math.e**Z1[j][i]/deno - 1
                # minout[i] += (Z1[j][i]/deno)**2
                # minout[i] += Z1[j][i]/deno
                # minout[i] += math.sqrt(Z1[j][i]/deno)
                minout[i] += (R) ** 0.5
                # minout[i] += -(deno/Z1[j][i] + 0.01) * (deno/Z1[j][i] + 0.01)
                # minout[i] += Z1[j][i]/deno + math.sqrt(Z1[j][i]/deno)
            # elif(R>=0):
            #     minout[i] += R
            elif(R<0):
                minout[i] += (-50000*R+len(Z1)*10) * 10
    min=1e9
    ret=0
    for i in range(n_h):
        #print(minout[i])
        if(minout[i]<min):
            min=minout[i]
            ret=i
    # print("loss:",min)
    a,b,c=parameters["W1"][ret]
    d=parameters["b1"][ret]
    print([a,b,c,d])
    r,theta,varphi = parameters["W"][ret]
    # print([r,theta / math.pi,varphi / math.pi])
    return r,theta,varphi

#cache是当前的模型，X不知道什么屌东西，rate学习率，i我猜应该是iteration
def backward_propagation(cache, X, rate, i):
    rate = rate * 0.5 ** (i // 10)
    li = []
    cache = np.array(cache)
    #TODO 这里要改写成球面坐标的形式
    for delta_r in [0.1, 0, -0.1]:
        for delta_theta in [0.1 * math.pi, 0, -0.1 * math.pi]:
            for delta_varphi in [0.2 * math.pi, 0, -0.2 * math.pi]:
                temp = [delta_r, delta_theta, delta_varphi]
                li.append(temp)
    li = np.array(li) * rate
    W = li[:, :3] + cache[:]
    W1 = []
    b1 = []
    for i in range(W.__len__()):
        r = W[i][0]
        theta = W[i][1]
        varphi = W[i][2]
        x = r * math.sin(theta) * math.cos(varphi)
        y = r * math.sin(theta) * math.sin(varphi)
        z = r * math.cos(theta)
        A = 0 - x
        B = 0 - y
        C = 0 - z
        D = -1 * x * A - y * B - z * C
        W1.append([A,B,C])
        b1.append([D])
    W1 = np.array(W1)
    b1 = np.array(b1)
    W = np.array(W)
    # print(W1)
    # print(b1)
    parameters = {"W1": W1, "b1": b1, "W": W}
    return parameters

def nn_model(X, num_iterations = 1000, print_cost=False):
    n_x = 3  #x,y,z
    n_h = 27 #定义隐藏层size
    n_y = 4  #a,b,c,d
    rate= 1
    #平面初始化得到球面点坐标
    parameters = initialize_parameters(X,n_x, n_h, n_y)
    for i in range(num_iterations):
        print("iteration",i+1)
        #正向传播的到Z = Ax + By + Cz + D
        Z1 = forward_propagation(X, parameters)
        #print(Z1)
        #反向传播过程得到的应该是loss最小的球面r，theta，varphi
        r,theta,varphi = compute_cost(Z1, n_h, parameters)
        cache=[r,theta,varphi]
        parameters = backward_propagation(cache, X, rate,i+1)
    return cache

def move_face(X,cache,threshold):
    r,theta,varphi = cache
    x = r * math.sin(theta) * math.cos(varphi)
    y = r * math.sin(theta) * math.sin(varphi)
    z = r * math.cos(theta)
    a = 0 - x
    b = 0 - y
    c = 0 - z
    d = -1 * x * a - y * b - z * c
    cnt=0
    deno=math.sqrt(a*a+b*b+c*c)
    for i in range(len(X)-1,-1,-1):
        if(a*X[i][0]+b*X[i][1]+c*X[i][2]+d<deno*threshold):
            X.remove(X[i])
            cnt+=1
    print("删除点数：",cnt)
    return X



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    li = read('F:\cscv\Plane optimal fit problem\models//facePointTarget.txt')

    # 归一化操作
    # min_max_scaler = preprocessing.MinMaxScaler()
    # X = min_max_scaler.fit_transform(X)

    face = 20
    epoch = 300
    thresold = 1e-3
    ans = []
    for i in range(face):
        if li.__len__() == 0:
            break
        X = np.array(li)
        # print(X)
        print("face:", i + 1)
        fig = plt.figure()
        ax = mplot3d.Axes3D(fig)
        ax.scatter3D(X.T[0], X.T[1], X.T[2])
        plt.show()
        cache = nn_model(X, epoch, True)
        li = move_face(li, cache, thresold)
        ans.append(cache)
        print(i)
    #输出结果
    print(ans)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import numpy as np
import random
from sklearn import preprocessing

'''
    描述：读取binvox文件并将结果还原成三维的状态
    参数：需要读取和改变的binvox文件
    返回：返回的是一个三维的ndarray，然后后续实在对应的ndarray上进行添加和修改的
'''
def turnThreeDiv(voxFile):
    with open(voxFile,'rb') as f:
        # 读取前五行，将指针定位到数据文件
        for i in range(5):
            f.readline()
        # 直接读取原始文件
        # 验证一下对应的文件指针是不是对的
        raw_data = np.frombuffer(f.read(), dtype=np.uint8)
        # 将是否出现和出现的此相互进行保存
        values, counts = raw_data[::2], raw_data[1::2]
        # 将之恢复成对应的0和1构成的np矩阵，默认是生成一维矩阵
        data = np.repeat(values,counts).astype(np.int)
        # 生成对应的三维矩阵
        coordinate = np.empty((128,128,128),dtype=int,order='C')
        # 将一维矩阵转成对应的三维矩阵,遍历对应的一维矩阵
        for i in range(data.size):
            x = i % 128
            # 获取y对应的坐标
            y = int(i / 128) % 128
            # 获取z1的坐标
            z = int(i / 128 / 128) % 128
            # p当前对应的x，y，z坐标
            coordinate[x][y][z]=data[i]
        # 将转储之后的三维矩阵进行输出
        return coordinate

'''
    描述：获取转化之后的三维坐标，获取三维模型的表面
    参数：输入三维坐标下体素文件，有就是1，没有就是0
    返回：返回的是一个三维点的list
    注意：对于30*40*50的立方体，全采样的点是64821
          六面体表面采样之后是9402个点
'''
def getSurface(coordinate):
    surface = []
    for i in range(128):
        for j in range(128):
            for k in range(128):
                #print(i,',',j,',',k)
                if(coordinate[i][j][k] == 1):
                    # 确定了在体素内部的点，判定再提速边缘的点,这里是确定在体素表面的点
                    if(i == 127 or j == 127 or k == 127 or
                            i == 0 or j == 0 or k == 0):
                        # 上述的判定是否已经遍历到的体素空间的边界点
                        surface.append([i,j,k])
                    else:
                        sum = coordinate[i][j][k+1]+ coordinate[i][j][k-1]\
                              +coordinate[i][j+1][k] + coordinate[i][j-1][k]\
                            +coordinate[i+1][j][k] + coordinate[i-1][j][k]
                        if(sum < 6 ):
                        # 如何对表面点进行稀疏化
                            point = [i,j,k]
                            surface.append(point)
    return surface



if __name__ == '__main__':

    # 获取特定路径体素文件中的表面的点，结果是[x,y,z]的形式
    result = getSurface(turnThreeDiv('./test/100100100box.binvox'))
    print(len(result))
    # 这里是均匀采样
    #result = result[0:-1:5]
    #result = random.sample(result,5000)
    #print(result)
    min_max_scaler = preprocessing.MinMaxScaler()
    result = min_max_scaler.fit_transform(result)
    result = [(x-0.5)*2 for x in result]
    print(result)
    #print(result)
    with open('./test/ballOrdinate.txt','w') as f:
        for i in result:
            temp = " ".join('%s' %id for id in i)+'\n'
            f.write(temp)
    print(len(result))
from sklearn import preprocessing

'''
    描述：计算点和面的距离
    参数：point是对应的点[x,y,z]
         face是对应的面的参数[a,b,c,d]
    返回：最终返回的是对应的距离
'''
def distance(point,face):
    up = abs(point[0]*face[0]+ point[1]*face[1]+point[2]*face[2]+face[3])
    down = face[0]**2+face[1]**2+face[2]**2+face[3]**2
    down = down ** 0.5
    return up/down

'''
    参数：points：对应的的参数列表【x,y,z】
         filename是文件保存的名字
    返回：最终返回的是对应的文件
'''
def normal(points,filename):
    path = './test/'+filename+'.txt'
    with open(path, 'a') as fp:
        for i in range(len(points)):
            fp.write(str(points[i][0]))
            fp.write(" ")
            fp.write(str(points[i][1]))
            fp.write(" ")
            fp.write(str(points[i][2]))
            fp.write(" ")
            fp.write(str(points[i][3]))
            fp.write(" ")
            fp.write(str(points[i][4]))
            fp.write(" ")
            fp.write(str(points[i][5]))
            fp.write("\n")


'''
    描述：生成相关的模型，传入相关的立方体的边长
    返回：返回对应的立方体的点构成的list
'''
def constructModel(a,b,c):
    result = list()
    min_max_scaler = preprocessing.MinMaxScaler()
    for i in range(a):
        for j in range(b):
            for k in range(c):
                temp = list()
                temp.append([i-50,j-50,k-50,0,0,0])
                temp = min_max_scaler.fit_transform(temp)
                result.append(temp[0])

    return result

'''
    参数：传入的是面构成的立方体
    返回：返回的是一个128*128*128空间的标注的点
    概述：在128*128*128空间中所有符合面的点
'''
def addFace(face):
    #print(face)
    result = list()
    temp =list()
    min_max_scaler = preprocessing.MinMaxScaler()

    # 采样点的范围是0-128，对对应的采样点进行
    for x in range(128):
        for y in range(128):
            for z in range(128):
                temp.append([x,y,z])

    # 生成对应的所有数据的点的集合
    temp = min_max_scaler.fit_transform(temp)

    for i in face:
        for j in temp:
            test = distance(j, i)
            if (test <= 0.01):
                # 根据颜色添加对应点
                result.append([j[0], j[1], j[2], int(i[0] * 200), int(i[1] * 200), int(i[2] * 200)])
    return result

'''
    描述：增加对应的点
    参数：originalBox是对应的原来的模型的参数
         face是对应表面的方程组
    返回：最终的结果是标记之后的点
'''
def addColor(orginalBox,face):
    result = list()
    for i in orginalBox:
        for j in face:
            point = [float(i[0]),float(i[1]),float(i[2])]
            temp = distance(point,j)
            if(temp<0.1):
                result.append([i[0],i[1],i[2],0,0,0])
    return result

'''
    描述：完成对两个模型的上色，输入的是两个模型的点，分别是以x,y,z的形式的txt文件
    参数：innerBox是模型上的点，即内部的点
          outerBox是体素空间中模型外部的点
    返回：
'''
def mixColor(innerBox,outerBox):

    # 将体素外的点和四
    result = list()

    # 遍历每一个点,内部的点标注为绿色
    for i in innerBox:
        # print(i)
        result.append([i[0],i[1],i[2],0,255,0])

    # 遍历每一个点，外部的点标注为红色
    for j in outerBox:
        # print(j)
        result.append([j[0],j[1],j[2],255,0,0])

    return result

'''
    描述：改变原来模型的颜色，使之使用不同的颜色进行展示,或者对原来没有颜色的模型进行添加颜色
    参数：输入的是txt文件，文件每一行的样式是x y z r g b
         color是指定的颜色，为[r,g,b]的列表，主要是为了区分你保存的文件
    返回：直接修改源文件，没有修改
'''
def changeColor(filename,color):
    result = list()
    with open(filename ,'r') as f:
        for line in f.readlines():
            # 这里你自己根据你需要的分隔符进行修改
            temp = line.strip().split(',')
            a = int(abs(float(temp[0]))*200)
            b = int(abs(float(temp[1]))*200)
            c = int(abs(float(temp[2]))*200)
            # print(a,b,c)

            if(len(temp) < 5):
                temp.append(a)
                temp.append(b)
                temp.append(c)
                print()
            else:
                temp[3] = a
                temp[4] = b
                temp[5] = c
           # print(temp)
            result.append(temp)

    # 将修改之后的文写入到原始的文件中
    filename = filename[6:13]+str(color[0])+str(color[1])+str(color[2])

    normal(result,filename)


if __name__ == '__main__':

    # 首先要添加原来的模型的颜色
    # 修改对应模型的颜色，你可以输入两种形式[x,y,z]和[x,y,z,r,g,b]
    changeColor('./test/EightFaceSurface.txt',[0,0,0])


     # 下述是获取对应表面方程
    facePoint = list()
    with open('./test/test.txt') as  f:
        for line in f.readlines():
            temp = list()
            # 逐个遍历对应每一行元素，将之转为对应的数据
            b = line.strip(",][").split(',')
            if (len(b) >= 5):
                b.pop()
            for a in b:
                a = a.replace('[', '').replace(']', '')
                temp.append(float(a))
                #print(temp)
            facePoint.append(temp)
            print(temp[3],'=',temp[0],'x+',temp[1],'y+',temp[2],'z')
    print('表面方程的数量',len(facePoint))
    # addFace(facePoint)


    ## 将原来的模型中的所有的表面点全部遍历一遍，将符合面的方程的点进行标红，体现面对模型表面的影响
    
    ## print('表面方程的数量',len(facePoint))
    facePoint = addFace(facePoint)
    print('最终标记点的数量',len(facePoint))
    ## 将原来的点进行保存，写入到对应文件中
    normal(facePoint,'facePointTragetEightFace')





























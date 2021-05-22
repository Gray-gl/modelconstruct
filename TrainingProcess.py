import visualizing

'''
    参数：points：对应的的参数列表【x,y,z，R，G，B】
         path是文件保存的路径
    返回：最终返回的是对应的文件
'''
def savePath(points,path):
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
    描述：对面的数据进行处理，根据你传入的文件名称，特定epoches的序列
    参数：filename输入的对应的面训练的过程中收集到的调整的数据结果
          step是需要输出的步长为step的epoch情况面的数据
    返回：特定数量面的参数构成的数组
'''
def handleFaceData(filename,step):
    result = list()
    with open(filename,'r') as f:
        # 读取仅仅读取平面的方程
        # 这句话是针对iteration1 换行  面的abcd参数
        # for line in f.readlines()[1::2]:
        # 下述对应的数据是：
        # [0.00026297944367824344, 0.0002427103578365869, 5.275577165566245, 8.792540934388082e-05],
        # [0.018210979018164875, -0.013935297705298944, -5.700518048607146, 5.713253391573144],
        for line in f.readlines():
            # 去除每一行开头的左右方括号，并且使用，进行分割
            temp = line.strip(',][ ').split(',')
            # 遍历每一行的数据，并清除对应的行左右括号的和空格
            temp2 = list()
            # 将清楚之后的数据保存到temp临时数组中，将数组保存到最终的结果中
            for i in temp:
                j = i.strip().replace('[', '').replace(']', '')
                #print(i)
                temp2.append(float(j))
            # 将结果保存到result中
            result.append(temp2)
            #print(temp)

    # 对已经生成的列表进行排序
    # print(len(result))
    result = result[0:110:step]
    return result

'''
    描述：将采样的模型的表面点，通过face方程进行判定，改变颜色，并将改变颜色之后的模型表面点保存到的path指定的路径中
    参数：原始的数据集pointSet,你的模型的表面点，输入对应的数据点集的文件路径
         面的参数face  [a,b,c,d]
         path最终结果保存的文件的路径，结果保存的是[x,y,z,r,g,b] 
    返回：没有返回
'''
def deleteFacePoint(pointSet,face,path):

    # 用来保存最终的结果
    result = list()

    # 遍历所有点，判断其和面之间的关系,并且修改对应点的颜色为红色色
    with open(pointSet,'r') as f:
        for point in f.readlines():
            point = point.strip().split()
            # 判定的点和face之间的关系
            # print(point,len(point))
            #count = count +1
            if(len(point) == 6):
                point = [float(x) for x in point]
                dist = visualizing.distance(point,face)
                if(dist <= 0.0005):
                    # 删除的点染成黑色
                    point[3] = 255
                    point[4] = 0
                    point[5] = 0
                    result.append(point)
                else:
                    result.append(point)
    #print('count:',count)
    #print('count2:',count2)

    print('加上面的点是',len(result))
    # 将面上的点和采样的点全部都保存到path的文件中
    savePath(result,path)


if __name__ == '__main__':

    # 读取保存面得参数的文件，按步长进行获取，获取对应的面的方程
    temp = handleFaceData('./test/test.txt',5)
    # 输出为方程的形式，是为了画出对应的方程的面
    for i in temp:
        print(i[3],'=',i[2],'x+',i[1],'y+',i[0],'z')

    # surfacepoint是对应的模型的表面点的集合，没有采样，是为了更好的显示出来
    surfacePoint = './test/EightFaceSurface.txt'
    # 注意，这里是遍历同一个面，输出到文件中
    for i in range(len(temp)):
        # path是同一个面的染色之后的模型的点保存的路径和随机生成的文件名
        path = './EightFace/faceOne'+str(i)+'.txt'
        print(temp[i])
        deleteFacePoint(surfacePoint,temp[i],path)





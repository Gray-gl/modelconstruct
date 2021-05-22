import struct

def read_header2(fp):
    # 读取binvox头文件
    headline = fp.readline()
    dims = fp.readline()
    translate = fp.readline()
    scale = fp.readline()
    dataline = fp.readline()
    return headline, dims, translate, scale, dataline

'''
    说明：将voxdata形成的数据变成对应的体素文件
'''
def savingdata(voxdata,filename):
    mypath = "../test/1.binvox"
    with open(mypath, 'rb') as f:
        headline, dims, translate, scale, dataline = read_header2(f)
    print("获取对应的文件头为： ", headline, dims, translate, scale, dataline)
    # 在这里修改输出的binvox文件路径和文件名
    savePath = "../test/"+filename+".binvox"
    with open(savePath, 'wb')as fp:
        # a = struct.pack('B', headline,dims,translate,scale,dataline)
        fp.write(headline)
        fp.write(dims)
        fp.write(translate)
        fp.write(scale)
        fp.write(dataline)
        for x in voxdata:
            'print(x)'
            a = struct.pack('B', x)
            'print(a)'
            fp.write(a)
    print("export data done")



'''
    描述：判定输入的点与标准几何面平行的面之间的关系
'''
def judge(x1,x2,y1,y2,z1,z2,x,y,z):
    a = x <= x2 and x >= x1
    b = y <= y2 and y >= y1
    c = z <= z2 and z >= z1
    return a and b and c

'''
    描述：判定输入的点和任意面之间的关系
    返回：如果为真，确定点在面下，如果为假，则点在面上
'''
def judge1(face,x,y,z):
    return face[0]*x+face[1]*y+face[2]*z+face[3] < 0

'''
    描述：生成对应的平面是ax+by+cz+d=0
    参数：平面的四个参数
    注意：这里是有一个问题的，那就是仅仅只能模拟第一象限，即xyz全部都是正的坐标
          在这里稍微进行一下修改
'''
def faceExport(a,b,c,d):
    # 生成128*128*128个点的体素三维空间
    filename = ""+str(a+b+c+d)
    voxdata = []
    for x in range(-64,64):
        for y in range(-64,64):
            for z in range(-64,64):
                'print(result)'
                test = a*x+b*y+c*z+d
                if (test >=  -0.05 and test <= 0.05):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    voxdata.append(1)
    savingdata(voxdata,filename)
    return filename




'''
    描述：生成对应长宽分别为a，b，c的六面体
    参数：参数为六面体的长宽高
'''
def boxExport(a,b,c):
    # 生成128*128*128个点的体素三维空间
    filename = ""+str(a)+str(b)+str(c)+"box"
    voxdata = []
    for x in range(-64,64):
        for y in range(-64,64):
            for z in range(-64,64):
                'print(result)'
                if (judge(0-a/2,a/2,0-b/2,b/2,0-c/2,c/2,x,y,z)):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    # 这里是增加计数的项，先是是否存在，然后就是对应的数量
                    voxdata.append(1)
    savingdata(voxdata,filename)

'''
    描述：生成球体
    参数：参数为半径
'''
def ballExport(r):
    # 生成128*128*128个点的体素三维空间
    filename = ""+str(r)+"ball"
    voxdata = []
    for z in range(-64,64):
        for y in range(-64,64):
            for x in range(-64,64):
                'print(result)'
                if (x*x+y*y+z*z <= r*r):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    voxdata.append(1)
    savingdata(voxdata,filename)

'''
    描述：生成对应四个面分别为对应方程的四面体
    参数：参数为四面体的四个方程
         第一个面是地面，后续三个面是对应的地面上面的三个面
'''
def traingleExport(face1,face2,face3,face4):
    # 生成128*128*128个点的体素三维空间
    filename = ""+str(face1)+"traingle"
    voxdata = []
    for z in range(-64,64):
        for y in range(-64,64):
            for x in range(-64,64):
                # 这里的是人工对点和面之间关系进行判定，并没有增加点在面内的关系
                if (judge1(face2,x,y,z) and not judge(face3,x,y,z)
                        and judge(face4,x,y,z) and not judge(face1,x,y,z)):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    # 这里是增加计数的项，先是是否存在，然后就是对应的数量
                    voxdata.append(1)
    savingdata(voxdata,filename)

'''
    描述：判定面和立方体的对于点的关系
    参数：face是所有面的参数构成的集合
         box是立方体三边构成得集合
         x，y，z是点的三个坐标轴
'''
def judgeFaceAndBox(face, box,x,y,z):

    # 判定点是否合理
    for i in face:
        test = x*i[0]+y*i[1]+z*i[2]+i[3]
        if(test <= 0.1 and test >= -0.1):
            return True

    # 判定立方体是否合理
    length = x <= box[0]
    width = y <= box[1]
    height = z <= box[2]
    res = length and width and height
    if(res):
        return True

    # 如果全部都没有满足，直接真
    return False


def faceAndBoxExport(face,box):
    # 生成128*128*128个点的体素三维空间
    filename = "tempresult";
    voxdata = []
    for x in range(128):
        for y in range(128):
            for z in range(128):
                'print(result)'
                if (judgeFaceAndBox(face,box,x,y,z)):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    voxdata.append(1)
    savingdata(voxdata,filename)
    return filename

'''
    描述：生成五角柱
    参数：参数为半径
'''
def EightFaceExport(r):
    # 生成128*128*128个点的体素三维空间
    filename = ""+str(r)+"EightFace"
    voxdata = []
    for z in range(-64,64):
        for y in range(-64,64):
            for x in range(-64,64):
                'print(result)'
                if (abs(x)+abs(y)+abs(z) <= r):
                    flag = 1
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    voxdata.append(1)
    savingdata(voxdata,filename)

'''
    描述：生成凹多面体模型，基本的是一个长方体的右下角挖了一个小长方体
    参数：outer是外围较大的长方体的三个长宽高构成得list，inner是内部较小的长方体的长宽高构成的list
    返回：最终保存为binvox文件
'''
def Concaveobject(outer,inner):
    filename = "" + str(outer[0]) + str(outer[1]) + str(outer[2])+str(inner[0])+str(inner[1])+str(inner[2]) + "box"
    voxdata = []
    for x in range(-64, 64):
        for y in range(-64, 64):
            for z in range(-64, 64):
                'print(result)'
                if (judge(0 - outer[0] / 2, outer[0] / 2, 0 - outer[1] / 2, outer[1] / 2, 0 - outer[2] / 2, outer[2] / 2, x, y, z)):
                    # 上述方法生成的是100*100*100的立方体，对其中的点进行筛选
                    if(not judge(outer[0] / 2-inner[0], outer[0] / 2,  outer[1] / 2-inner[1], outer[1] / 2,outer[2] / 2 - inner[2], outer[2] / 2, x, y, z)):
                         flag = 1
                    else:
                        # 如果生成的不是在立方体的内部，就将之置为零
                        flag = 0
                else:
                    flag = 0
                if (len(voxdata) > 0 and flag == voxdata[-2] and voxdata[-1] < 255):
                    voxdata[-1] += 1
                else:
                    voxdata.append(flag)
                    # 这里是增加计数的项，先是是否存在，然后就是对应的数量
                    voxdata.append(1)
    savingdata(voxdata, filename)


if __name__ == '__main__':
    # 将对应的参数文件进行读取，获取其中每一项
   Concaveobject([100,100,100],[60,60,60])



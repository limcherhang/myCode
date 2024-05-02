import matplotlib.pyplot as plt
import numpy as np

def draw1():
    t_values = np.linspace(0,10*np.pi, 1000)

    x_values = 8*np.cos(t_values)-6*np.cos(8*t_values/3)

    y_values = 8 * np.sin(t_values) - 6*np.sin(8*t_values/3)

    plt.plot(x_values, y_values, label='many circle plot')

    plt.savefig('1.png')
    plt.close()

draw1()

def draw2():
    # 生成 t 值
    t_values = np.linspace(0, 2*np.pi, 30)  # 避免 tan 和 cot 的值无穷大

    # 计算 r 值
    r_values = 20 * (np.tan(17 * t_values) + 1/np.tan(17 * t_values))

    x_values = r_values*np.cos(t_values)
    y_values = r_values*np.sin(t_values)

    # 绘制极坐标图形
    plt.plot(x_values, y_values, label='r = 20 * (tan(17t) + cot(17t))')
    
    plt.savefig('2.png')
    plt.close()

draw2()

def draw3():

    xs = np.linspace(-10,10,1000)
    ys = np.linspace(-10,10,1000)

    x, y = np.meshgrid(xs, ys)

    z = y**2 - x**2 * (np.sin(x)+y)/(np.sin(y)+x)

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('3.png')
    plt.close()

draw3()

def draw4():
    ts = np.linspace(0, 30, 1000)

    xs = 2 * np.cos(ts) + 5 * np.cos(2*ts/3)
    ys = 2 * np.sin(ts) - 5 * np.sin(2*ts/3)

    plt.plot(xs, ys)
    plt.savefig('4.png')
    plt.close()

draw4()

def draw5():
    xs = np.linspace(-10, 10, 1000)
    ys = np.linspace(-10, 10, 1000)

    x, y = np.meshgrid(xs, ys)

    z = np.sin(x**2)-np.sin(y**2)
    
    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('5.png')
    plt.close()

draw5()

def draw6():
    ts = np.linspace(0, 10*np.pi, 1000000)

    rs = np.exp(np.sin(ts)) - 2 * np.cos(4*ts) + np.sin((4*ts-np.pi)/24)**5

    xs = rs * np.cos(ts)
    ys = rs * np.sin(ts)

    # 绘制极坐标图形
    plt.plot(xs, ys)
    
    plt.savefig('6.png')
    plt.close()

draw6()

def draw7():
    xs = np.linspace(-10, 10, 1000)
    ys = np.linspace(-10, 10, 1000)

    x, y = np.meshgrid(xs, ys)

    z = y - x * np.sin(x**2+y**2)

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('7.png')
    plt.close()

draw7()

def draw8():
    xs = np.linspace(-30, 30, 1000)
    ys = np.linspace(-30, 30, 1000)

    x, y = np.meshgrid(xs, ys)

    z = y * np.sin(y) - x * np.sin(x)

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('8.png')
    plt.close()

draw8()


def draw9():
    xs = np.linspace(-10, 10, 1000)
    ys = np.linspace(-10, 10, 1000)

    x, y = np.meshgrid(xs, ys)

    z = 2**(np.sin(x)+np.cos(y)) - np.exp(np.sin(x*y))

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('9.png')
    plt.close()

draw9()

def draw10():
    xs = np.linspace(-20, 20, 1000)
    ys = np.linspace(-20, 20, 1000)

    x, y = np.meshgrid(xs, ys)

    z = y - x * np.sin(np.sin(x)/np.sin(y))

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('10.png')
    plt.close()

draw10()

def draw11():
    xs = np.linspace(-10, 10, 1000)
    ys = np.linspace(-10, 10, 1000)

    x, y = np.meshgrid(xs, ys)

    z = y * np.sin(x**2) - x * np.sin(y**2)

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('11.png')
    plt.close()

draw11()

def draw12():
    xs = np.linspace(-10, 10, 1000)
    ys = np.linspace(-10, 10, 1000)

    x, y = np.meshgrid(xs, ys)

    z = np.sin(x**2+y**2) - np.tan(np.sin(x+y))

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('12.png')
    plt.close()

draw12()

def draw13():
    xs = np.linspace(-8, 8, 1000)
    ys = np.linspace(-8, 8, 1000)

    x, y = np.meshgrid(xs, ys)

    z = np.tan(x**2*np.sin(y**2)) - np.tan(y**2*np.sin(x**2))

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('13.png')
    plt.close()
draw13()

def draw14():
    xs = np.linspace(-8, 8, 1000)
    ys = np.linspace(-8, 8, 1000)

    x, y = np.meshgrid(xs, ys)

    z = np.tan(x**2+y**2) * np.cos(x+y) - np.cos(y**2+x**2)

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('14.png')
    plt.close()
draw14()

def draw15():
    xs = np.linspace(-8, 8, 10000)
    ys = np.linspace(-8, 8, 10000)

    x, y = np.meshgrid(xs, ys)

    z = np.tan(x*np.sin(x))-np.tan(y*np.sin(y))

    plt.contour(x, y, z, levels=[0], colors='r')

    plt.savefig('15.png')
    plt.close()

draw15()
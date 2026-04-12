# 继承
# 父类与子类——父类可以有多个子类，子类也可以有多个父类
# 子类的定义：class 子类(父类1，父类2，……)

# 父类
class People:
    def SetName(self, name):
        self.name = name
    def __init__(self, name):
        self.name = name
    def PrintInfo(self):
        print("姓名为%s"%self.name)
    def CaptureImage(self):
        print("People类中的CaptureImage方法被调用!")

# 子类：父类为子类的参数
class Student(People):
    def SetSno(self, no):
        self.sno = no
    def __init__(self, name, no):  # 方法重写
        self.name = name
        self.sno = no
    def PrintInfo(self):
        print("姓名为%s, 学号为%s"%(self.name, self.sno))
    def CaptureImage(self):
        print("Student类中的CaptureImage方法被调用!")

# 单继承
class Teather(People):
    def SetTno(self, no):
        self.tno = no
    def __init__(self, name, no):
        # ↓ super方法：在子类中使用父类的方法
        super().__init__(name)
        self.tno = no

# 多继承
class PD(Student, Teather):
    def SetPD(self, pd):
        self.pd = pd

# 多态
def PrintPersonInfo(People):
    return People.PrintInfo()

# 鸭子类型
def CaptureImageTest(arg):
    arg.CaptureImage()

# 一些内置函数：
# isinstance: 判断一个对象是否是一个类或其子类的实例
# issubclass: 判断一个类是否是另一个类的子类
# type: 判断对象所属的类


class Complex:
    def __init__(self, real, image):
        self.real = real
        self.image = image
    # 类方法：用@classmethod修饰的方法，可以通过类名调用，也可以通过实例对象调用
    @classmethod
    def add(cls, c1, c2):
        c = Complex()
        c.real = c1.real + c2.real
        c.image = c1.image + c2.image
        return c
    # 静态方法：和类方法相似，但没有第一个cls参数
    @staticmethod
    def add(c1, c2):
        c = Complex(0, 0)
        c.real = c1.real + c2.real
        c.image = c1.image + c2.image
        return c


if __name__ == "__main__":
    p = People("张三")
    stu = Student("张三", "1810100")
    # p.PrintInfo()
    # stu.PrintInfo()
    PrintPersonInfo(p)
    PrintPersonInfo(stu)
    CaptureImageTest(p)
    CaptureImageTest(stu)
    print("-"*25)
    c1 = Complex(2.5, 1.5)
    c2 = Complex(1.7, 1.8)
    c = Complex.add(c1, c2)
    print("c1+c2=%.2f+%.2fi"%(c.real, c.image))

# 面向对象编程(OOP)
# 类与对象:类——抽象，对象——具体


# 创建一个类名为Student的类
class Student:
    name = "unknown"
    age = 18
    # 私有属性：只能在类的内部访问
    __id = 'XXXXXXXXXX'

    # 定义类的普通方法：只能通过实例调用，不能通过类名调用
    def SetName(self, newname):# self自动调用不需传入参数
        self.name = newname
    def PrintName(self):
        print("name:%s"%self.name)
    # 使用方法使私有属性在类外可以被访问
    def SetID(self, newid):
        self.__id = newid
    def PrintID(self):
        print("name:%s"%self.__id)
    
    # 构造方法：对象构建时自动调用
    def __init__(self):
        print("构造方法被调用！")
        # self.name = name
    
    # 析构方法：销毁类对象时自动执行
    def __del__(self):
        print("姓名为%s的对象被销毁"%self.name)
    
    # 内置方法
    def __str__(self):
        return "这个类是我写的^_^"
    def __len__(self):
        return 10


# 用类名访问
print(Student.name)
print("-"*20)

# 用对象访问
stu1 = Student()
stu1.name = "Bob"
print(stu1.name)

# 动态绑定新属性
stu1.no = '10001'
print(stu1.no)  # 用对象不报错
# print(Student.no)  # 用类名会报错

# 使用方法
stu1.SetName("Tom")
stu1.PrintName()
del stu1

print("-"*20)
stu2 = Student()
stu2.SetName("Alice")
stu2.PrintName()
stu3 = stu2 # 复制的是指针，而不是直接赋值
stu2.SetName("Zed")
stu2.PrintName()
stu3.PrintName()
del stu2
del stu3

# 使用内置方法
print("-"*20)
stu4 = Student()
print(stu4)
print(len(stu4))


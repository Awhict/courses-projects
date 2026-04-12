# 动态拓展类与实例
from types import MethodType

class Student:
    # 装饰器
    @property  # 设置读方法（读权限）
    def score(self):
        return self._score  # 属性前加_是为了防止递归调用
    @score.setter  # 设置写方法（写权限）
    def score(self, score):
        if score < 0 or score > 100:
            print("")
        else:
            self._score = score

def SetName(self, name):
    self.name = name

def SetSno(self, no):
    self.sno = no

stu1 = Student()
stu2 = Student()

# 为实例对象绑定方法：用MethodTpye
stu1.SetName = MethodType(SetName, stu1)
stu1.SetName("")

# 为类绑定方法：直接赋值
Student.SetSno = SetSno
stu1.SetSno("1810100")
stu2.SetSno("1810101")

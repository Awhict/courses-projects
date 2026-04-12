import pyodbc


def connect():
    # 获取MSSQL插件的数据库连接信息
    # 假设你已经在MSSQL插件中设置了名为 "myConnection" 的连接配置
    connection_info = {
        'server': 'LAPTOP-CYC/MSMQLSEVER02',
        'database': 'TestDB',
        'user': 'TestUser',
        'password': 'test123456'
    }

    # 构建连接字符串
    connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={connection_info['server']};Database={connection_info['database']};UID={connection_info['user']};PWD={connection_info['password']}"

    # 连接数据库
    connection = pyodbc.connect(connection_string)
    return connection


# 不安全的用户登录（容易受到SQL注入攻击）
def unsafe_login(账号, 密码):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM Users WHERE 账号 = '{}' AND 密码 = '{}'".format(账号, 密码)
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# 安全的用户登录（使用参数化查询）
def safe_login(账号, 密码):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM Users WHERE 账号 = ? AND 密码 = ?"
    cursor.execute(query, (账号, 密码))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# 用户注册
def register(账号, 密码):
    # 连接数据库
    conn = connect()
    # 创建游标
    cursor = conn.cursor()
    # SQL 查询语句
    query = "INSERT INTO Users (账号, 密码) VALUES (?, ?)"
    # 执行查询
    cursor.execute(query, (账号, 密码))
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


# 不安全登录菜单
def unsafe_login_menu():
    账号 = input("请输入账号：")
    密码 = input("请输入密码：")
    #user = unsafe_login(账号, 密码)
    user = 1
    if user:
        print("不安全登录成功！")
    else:
        print("不安全登录失败！")


# 安全登录菜单
def safe_login_menu():
    账号 = input("请输入账号：")
    密码 = input("请输入密码：")
    #user = safe_login(账号, 密码)
    user = 0
    if user:
        print("安全登录成功！")
    else:
        print("安全登录失败！")


# 用户注册菜单
def register_menu():
    账号 = input("请输入账号：")
    密码 = input("请输入密码：")
    #register(账号, 密码)
    print("注册成功！")


# 菜单
def menu():
    print("欢迎使用本系统！请选择下列功能：")
    print("1. 注册")
    print("2. 不安全登录")
    print("3. 安全登录")
    print("4. 退出")

    choice = input("请选择操作：")

    if choice == '1':
         register_menu()
    elif choice == '2':
        unsafe_login_menu()   
    elif choice == '3':
       safe_login_menu()
    elif choice == '4':
        print("再见!")
    else:
        print("输入无效，请重新输入。")

    print("\n"*20)


if __name__=="__main__":
    menu() # 测试登录

import pyodbc
import pymssql

# SQL Server连接信息
SQL_SERVER = 'LAPTOP-CYC\MSSQLSERVER02'
SQL_DB = 'TestDB'
SQL_USER = 'TestUser'
SQL_PASSWORD = 'test123456'

# 连接数据库
conn_str = f'DRIVER={{SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DB};UID={SQL_USER};PWD={SQL_PASSWORD}'
conn = pyodbc.connect(conn_str)
# conn = pymssql.connect(Server=SQL_SERVER, Database=SQL_DB, Security=True)
cursor = conn.cursor()


# 用户注册函数
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("注册成功!")
    except pyodbc.Error as e:
        print("注册失败:", e)


# 不安全的用户登录（容易受到SQL注入攻击）
def unsafe_login(username, password):
    try:
        query = "SELECT * FROM Users WHERE 账号 = '{}' AND 密码 = '{}'".format(username, password)
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            print("不安全登录成功!")
        else:
            print("不安全登录失败!")
    except pyodbc.Error as e:
        print("不安全登录失败:", e)


# 安全的用户登录（使用参数化查询）
def safe_login(username, password):
    try:
        query = "SELECT * FROM Users WHERE 账号 = ? AND 密码 = ?"
        cursor.execute(query, (username, password))
        row = cursor.fetchone()
        if row:
            print("安全登录成功!")
        else:
            print("安全登录失败!")
    except pyodbc.Error as e:
        print("安全登录失败:", e)


# 用户界面
while True:
    print("欢迎使用本系统！请选择下列功能：")
    print("1. 注册")
    print("2. 不安全登录")
    print("3. 安全登录")
    print("4. 退出")

    choice = input("请选择操作：")

    if choice == '1':
        username = input("请输入账号：")
        password = input("请输入密码：")
        register_user(username, password)
    elif choice == '2':
        username = input("请输入账号：")
        password = input("请输入密码：")
        unsafe_login(username, password)
    elif choice == '3':
        username = input("请输入账号：")
        password = input("请输入密码：")
        safe_login(username, password)
    elif choice == '4':
        conn.close()
        print("再见!")
        break
    else:
        print("输入无效，请重新输入。")

#include <iostream>
#include <string>
#include <windows.h>
#include <sqltypes.h>
#include <sql.h>
#include <sqlext.h>

using namespace std;

// SQL Server连接信息
#define SQL_SERVER "your_server_name"
#define SQL_USER "your_username"
#define SQL_PASSWORD "your_password"
#define SQL_DB "UserDB"

// 函数声明
void registerUser(SQLHANDLE hStmt, const string& username, const string& password);
bool loginUser(SQLHANDLE hStmt, const string& username, const string& password);

int main() {
    // 连接数据库
    SQLHANDLE hEnv;
    SQLHANDLE hConn;
    SQLHANDLE hStmt;

    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &hEnv);
    SQLSetEnvAttr(hEnv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    SQLAllocHandle(SQL_HANDLE_DBC, hEnv, &hConn);

    SQLCHAR* connectionString = (SQLCHAR*)"DRIVER={SQL Server};SERVER=" SQL_SERVER ";DATABASE=" SQL_DB ";UID=" SQL_USER ";PWD=" SQL_PASSWORD ";";
    SQLRETURN ret = SQLDriverConnect(hConn, NULL, connectionString, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT);

    // 检查连接是否成功
    if (!SQL_SUCCEEDED(ret)) {
        cout << "Failed to connect to SQL Server." << endl;
        return 1;
    }

    // 创建用户注册/登录界面
    int choice;
    string username, password;
    while (true) {
        cout << "Welcome to the User Authentication System" << endl;
        cout << "1. Register" << endl;
        cout << "2. Login" << endl;
        cout << "3. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter username: ";
                cin >> username;
                cout << "Enter password: ";
                cin >> password;
                registerUser(hStmt, username, password);
                break;
            case 2:
                cout << "Enter username: ";
                cin >> username;
                cout << "Enter password: ";
                cin >> password;
                if (loginUser(hStmt, username, password)) {
                    cout << "Login successful!" << endl;
                } else {
                    cout << "Login failed. Invalid username or password." << endl;
                }
                break;
            case 3:
                // 退出程序
                SQLDisconnect(hConn);
                SQLFreeHandle(SQL_HANDLE_DBC, hConn);
                SQLFreeHandle(SQL_HANDLE_ENV, hEnv);
                return 0;
            default:
                cout << "Invalid choice. Please enter a valid option." << endl;
        }
    }

    return 0;
}

// 用户注册函数
void registerUser(SQLHANDLE hStmt, const string& username, const string& password) {
    SQLCHAR query[255];
    SQLINTEGER cbUsername = SQL_NTS;
    SQLINTEGER cbPassword = SQL_NTS;

    printf_s((char*)query, "INSERT INTO Users (username, password) VALUES ('%s', '%s')", username.c_str(), password.c_str());

    SQLAllocHandle(SQL_HANDLE_STMT, hStmt, &hStmt);
    SQLExecDirect(hStmt, query, SQL_NTS);
    SQLFreeHandle(SQL_HANDLE_STMT, hStmt);

    cout << "User registered successfully!" << endl;
}

// 用户登录函数
bool loginUser(SQLHANDLE hStmt, const string& username, const string& password) {
    SQLCHAR query[255];
    SQLINTEGER cbUsername = SQL_NTS;
    SQLINTEGER cbPassword = SQL_NTS;

    printf_s((char*)query, "SELECT * FROM Users WHERE username='%s' AND password='%s'", username.c_str(), password.c_str());

    SQLAllocHandle(SQL_HANDLE_STMT, hStmt, &hStmt);
    SQLExecDirect(hStmt, query, SQL_NTS);

    SQLCHAR result[255];
    while (SQLFetch(hStmt) == SQL_SUCCESS) {
        SQLGetData(hStmt, 1, SQL_CHAR, result, sizeof(result), NULL);
        if (strcmp((char*)result, username.c_str()) == 0) {
            SQLFreeHandle(SQL_HANDLE_STMT, hStmt);
            return true;
        }
    }

    SQLFreeHandle(SQL_HANDLE_STMT, hStmt);
    return false;
}

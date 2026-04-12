package client;

import java.io.IOException;
import java.awt.AWTException;
import java.sql.SQLException;
import manager.DatabaseManager;

public class ClientMain {
    public static void main(String[] args) {
        // 数据库连接参数
        String dbURL = "jdbc:sqlserver://10.122.239.180:1433;databaseName=CStest;encrypt=false";
        String dbUser = "TestUser";
        String dbPassword = "Abc12345678";

        try {
            DatabaseManager dbManager = new DatabaseManager(dbURL, dbUser, dbPassword);

            // 显示登录注册窗口
            LoginRegisterGUI loginRegisterGUI = new LoginRegisterGUI(dbManager);
            loginRegisterGUI.setVisible(true);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void startClient(String username, DatabaseManager dbManager) {
        // 设置服务器IP、端口号和默认的监控频率
        String serverIP = "10.122.239.180"; // 服务器IP地址，指向本地
        int serverPort = 12345; // 服务器端口号，必须与服务器端匹配
        int captureInterval = 1000; // 默认的监控频率（以毫秒为单位）

        try {
            // 创建Client对象
            Client client = new Client(serverIP, serverPort, username, "testpassword", "10.122.239.180", "00:11:22:33:44:55", captureInterval);

            // 创建并显示客户端GUI
            ClientGUI clientGUI = new ClientGUI(client);
            clientGUI.setVisible(true);

            // 初始化系统托盘管理器
            SystemTrayManager systemTrayManager = new SystemTrayManager(client);
        } catch (IOException | AWTException e) {
            e.printStackTrace();
        }
    }
}

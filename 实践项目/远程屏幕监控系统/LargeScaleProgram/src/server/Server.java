package server;

import manager.DatabaseManager;

public class Server {
    public static void main(String[] args) {
        int port = 12345;
        try {
            DatabaseManager dbManager = new DatabaseManager("jdbc:sqlserver://localhost:1433;databaseName=CStest;encrypt=false", "TestUser", "Abc12345678");
            ServerGUI serverGUI = new ServerGUI();
            serverGUI.setVisible(true);

            ImageReceiver receiver = new ImageReceiver(port, serverGUI, dbManager);
            receiver.start();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

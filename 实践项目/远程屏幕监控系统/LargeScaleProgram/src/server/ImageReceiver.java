package server;

import javax.net.ssl.*;
import java.net.Socket;
import manager.DatabaseManager;

public class ImageReceiver {
    private int port;
    private ServerGUI serverGUI;
    private DatabaseManager dbManager;

    public ImageReceiver(int port, ServerGUI serverGUI, DatabaseManager dbManager) {
        this.port = port;
        this.serverGUI = serverGUI;
        this.dbManager = dbManager;
    }

    public void start() {
        try {
            SSLContext sslContext = SSLServerContext.getSSLContext();
            SSLServerSocketFactory ssf = sslContext.getServerSocketFactory();
            SSLServerSocket serverSocket = (SSLServerSocket) ssf.createServerSocket(port);
            serverSocket.setNeedClientAuth(true);

            while (true) {
                SSLSocket clientSocket = (SSLSocket) serverSocket.accept();
                new Thread(new ClientHandler(clientSocket, serverGUI, dbManager)).start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

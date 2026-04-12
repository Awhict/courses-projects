package server;

import javax.net.ssl.SSLSocket;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;
import manager.DatabaseManager;

public class ClientHandler implements Runnable {
    private SSLSocket clientSocket;
    private ObjectInputStream input;
    private ObjectOutputStream output;
    private ServerGUI serverGUI;
    private DatabaseManager dbManager;
    private static final String SCREENSHOT_DIR = "screenshots";
    private String clientAddress;

    public ClientHandler(SSLSocket clientSocket, ServerGUI serverGUI, DatabaseManager dbManager) {
        this.clientSocket = clientSocket;
        this.serverGUI = serverGUI;
        this.dbManager = dbManager;
        this.clientAddress = clientSocket.getInetAddress().toString();
        createScreenshotDir();
        serverGUI.registerClientHandler(clientAddress, this); // 注册 ClientHandler
    }

    private void createScreenshotDir() {
        File directory = new File(SCREENSHOT_DIR);
        if (!directory.exists()) {
            directory.mkdir();
        }
    }

    private String getScreenshotFilePath() {
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        return SCREENSHOT_DIR + File.separator + "screenshot_" + timestamp + ".jpg";
    }

    private void saveScreenshot(byte[] imageBytes) {
        try {
            String filePath = getScreenshotFilePath();
            try (FileOutputStream fos = new FileOutputStream(filePath)) {
                fos.write(imageBytes);
            }
            System.out.println("Screenshot saved: " + filePath);
            serverGUI.log("Screenshot saved: " + filePath); // 记录日志
        } catch (Exception e) {
            e.printStackTrace();
            serverGUI.log("Error saving screenshot: " + e.getMessage()); // 记录日志
        }
    }

    @Override
    public void run() {
        try {
            clientSocket.startHandshake(); // 执行 SSL 握手
            input = new ObjectInputStream(clientSocket.getInputStream());
            output = new ObjectOutputStream(clientSocket.getOutputStream());
            serverGUI.updateUserTree(clientAddress, true); // 用户上线
            serverGUI.log("Client connected: " + clientAddress); // 记录日志

            while (true) {
                Object received = input.readObject();
                if (received instanceof byte[]) {
                    byte[] imageBytes = (byte[]) received;
                    serverGUI.updateImage(clientAddress, imageBytes);
                    dbManager.insertScreenshot(clientAddress, imageBytes);
                    saveScreenshot(imageBytes);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            serverGUI.log("Error: " + e.getMessage()); // 记录日志
        } finally {
            serverGUI.updateUserTree(clientAddress, false); // 用户下线
            serverGUI.log("Client disconnected: " + clientAddress); // 记录日志
        }
    }

    public void sendCaptureIntervalUpdate(int newInterval) {
        try {
            output.writeObject(newInterval);
            output.flush();
            serverGUI.log("Capture interval updated to: " + newInterval + " ms for " + clientAddress); // 记录日志
        } catch (IOException e) {
            e.printStackTrace();
            serverGUI.log("Error sending capture interval update: " + e.getMessage()); // 记录日志
        }
    }
}

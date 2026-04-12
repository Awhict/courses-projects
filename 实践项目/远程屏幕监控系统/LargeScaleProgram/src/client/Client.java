package client;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.util.Timer;
import java.util.TimerTask;
import java.awt.AWTException;


public class Client {
    private SSLSocket socket;
    private ObjectOutputStream output;
    private ObjectInputStream input;
    private String serverAddress;
    private int port;
    public int captureInterval;
    private ScreenCapture screenCapture;
    private Timer timer;
    private SystemTrayManager trayManager;
    private ClientGUI clientGUI;

    public Client(String serverAddress, int port, String username, String password, String ip, String mac, int captureInterval) throws IOException, AWTException {
        this.serverAddress = serverAddress;
        this.port = port;
        this.screenCapture = new ScreenCapture();
        this.trayManager = new SystemTrayManager(this);
        this.captureInterval = captureInterval;
    }

    public void connect() throws IOException {
        SSLSocketFactory sslSocketFactory = null;
		try {
			sslSocketFactory = SSLClientContext.getSSLContext().getSocketFactory();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        socket = (SSLSocket) sslSocketFactory.createSocket(serverAddress, port);
        socket.startHandshake(); // 执行 SSL 握手
        output = new ObjectOutputStream(socket.getOutputStream());
        input = new ObjectInputStream(socket.getInputStream()); // 初始化输入流
        System.out.println("Connected to server at " + serverAddress + ":" + port);
        trayManager.displayMessage("Connection", "Connected to server at " + serverAddress + ":" + port);
        startScreenCapture();
        listenForIntervalUpdates(); // 启动监听截屏频率更新的方法
    }

    public void disconnect() throws IOException {
        if (timer != null) {
            timer.cancel();
        }
        if (socket != null && !socket.isClosed()) {
            socket.close();
            System.out.println("Disconnected from server.");
            trayManager.displayMessage("Disconnection", "Disconnected from server.");
        }
    }

    private void startScreenCapture() {
        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                try {
                    byte[] screenshot = screenCapture.captureScreen();
                    output.writeObject(screenshot);
                    output.flush();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }, 0, captureInterval); // Capture screen every interval
    }

    // 新增方法：监听截屏频率的更新
    private void listenForIntervalUpdates() {
        new Thread(() -> {
            while (true) {
                try {
                    Object received = input.readObject();
                    if (received instanceof Integer) {
                        int newInterval = (Integer) received;
                        updateCaptureInterval(newInterval);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    private void updateCaptureInterval(int newInterval) {
        captureInterval = newInterval;
        if (timer != null) {
            timer.cancel();
        }
        startScreenCapture();
    }

    public SystemTrayManager getSystemTrayManager() {
        return trayManager;
    }

    public void setClientGUI(ClientGUI clientGUI) {
        this.clientGUI = clientGUI;
    }

    public ClientGUI getClientGUI() {
        return clientGUI;
    }
}

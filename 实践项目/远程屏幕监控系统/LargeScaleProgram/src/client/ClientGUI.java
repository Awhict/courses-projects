package client;

import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JLabel;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Toolkit;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;

public class ClientGUI extends JFrame {
    private Client client;
    private JLabel statusLabel;

    public ClientGUI(Client client) {
        this.client = client;
        setTitle("远程屏幕监控系统 - 客户端");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE); // 修改关闭操作为隐藏窗口

        // 设置窗口居中
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int x = (screenSize.width - getWidth()) / 2;
        int y = (screenSize.height - getHeight()) / 2;
        setLocation(x, y);

        // 创建按钮
        JButton connectButton = new JButton("Connect");
        connectButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    client.connect();
                    updateStatusLabel("状态: 已连接");
                } catch (IOException ex) {
                    ex.printStackTrace();
                    updateStatusLabel("状态: 连接失败");
                }
            }
        });

        JButton disconnectButton = new JButton("Disconnect");
        disconnectButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    client.disconnect();
                    updateStatusLabel("状态: 已断开连接");
                } catch (IOException ex) {
                    ex.printStackTrace();
                    updateStatusLabel("状态: 断开连接失败");
                }
            }
        });

        // 创建状态标签
        statusLabel = new JLabel("状态: 未连接");

        // 创建面板并添加组件
        JPanel buttonPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        buttonPanel.add(connectButton, gbc);
        gbc.gridy = 1;
        buttonPanel.add(disconnectButton, gbc);

        // 使用 BorderLayout 布局
        setLayout(new BorderLayout());
        add(buttonPanel, BorderLayout.CENTER);
        add(statusLabel, BorderLayout.SOUTH);

        // 添加窗口关闭事件，最小化到托盘
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                setVisible(false);
                client.getSystemTrayManager().displayMessage("Client", "Application minimized to tray.");
            }
        });

        // 设置ClientGUI实例
        client.setClientGUI(this);
    }

    // 更新状态标签的方法
    private void updateStatusLabel(String status) {
        statusLabel.setText(status);
    }
}

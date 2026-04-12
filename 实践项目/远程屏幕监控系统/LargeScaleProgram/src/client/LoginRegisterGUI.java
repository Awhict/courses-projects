package client;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import manager.DatabaseManager;

public class LoginRegisterGUI extends JFrame {
    private JTextField usernameField;
    private JPasswordField passwordField;
    private JTextField ipField;
    private JTextField macField;
    private JButton loginButton;
    private JButton registerButton;
    private DatabaseManager dbManager;

    public LoginRegisterGUI(DatabaseManager dbManager) {
        this.dbManager = dbManager;
        setTitle("远程屏幕监控系统 - 客户端");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null); // 居中显示

        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);

        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("用户名:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.WEST;
        usernameField = new JTextField(20);
        panel.add(usernameField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("密码:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.WEST;
        passwordField = new JPasswordField(20);
        panel.add(passwordField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("主机 IP 地址:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 2;
        gbc.anchor = GridBagConstraints.WEST;
        ipField = new JTextField(20);
        panel.add(ipField, gbc);

        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.anchor = GridBagConstraints.EAST;
        panel.add(new JLabel("主机 MAC 地址:"), gbc);

        gbc.gridx = 1;
        gbc.gridy = 3;
        gbc.anchor = GridBagConstraints.WEST;
        macField = new JTextField(20);
        panel.add(macField, gbc);

        // Create a new panel for the buttons with a GridBagLayout
        JPanel buttonPanel = new JPanel(new GridBagLayout());
        GridBagConstraints buttonGbc = new GridBagConstraints();
        buttonGbc.insets = new Insets(0, 20, 0, 20);

        buttonGbc.gridx = 0;
        buttonGbc.gridy = 0;
        loginButton = new JButton("登录");
        buttonPanel.add(loginButton, buttonGbc);

        buttonGbc.gridx = 1;
        buttonGbc.gridy = 0;
        registerButton = new JButton("注册");
        buttonPanel.add(registerButton, buttonGbc);

        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(buttonPanel, gbc);

        add(panel);

        loginButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    String username = usernameField.getText();
                    String password = new String(passwordField.getPassword());
                    String ip = ipField.getText();
                    String mac = macField.getText();
                    if (dbManager.loginUser(username, password, ip, mac)) {
                        JOptionPane.showMessageDialog(null, "Login successful");
                        dispose();
                        ClientMain.startClient(username, dbManager);
                    } else {
                        JOptionPane.showMessageDialog(null, "Invalid username, password, IP or MAC address");
                    }
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
        });

        registerButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    String username = usernameField.getText();
                    String password = new String(passwordField.getPassword());
                    String ip = ipField.getText();
                    String mac = macField.getText();
                    if (dbManager.registerUser(username, password, ip, mac)) {
                        JOptionPane.showMessageDialog(null, "Registration successful");
                    } else {
                        JOptionPane.showMessageDialog(null, "Registration failed");
                    }
                } catch (SQLException ex) {
                    ex.printStackTrace();
                }
            }
        });
    }
}

package client;

import java.awt.AWTException;
import java.awt.Image;
import java.awt.MenuItem;
import java.awt.PopupMenu;
import java.awt.SystemTray;
import java.awt.TrayIcon;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.ImageIcon;

public class SystemTrayManager {
    private TrayIcon trayIcon;
    private Client client;

    public SystemTrayManager(Client client) throws AWTException {
        this.client = client;
        if (SystemTray.isSupported()) {
            SystemTray tray = SystemTray.getSystemTray();
            Image image = new ImageIcon("src\\client\\Page.png").getImage(); // 使用你提供的图标路径
            trayIcon = new TrayIcon(image, "远程屏幕监控系统 - 客户端");
            trayIcon.setImageAutoSize(true);

            // 添加点击事件以还原窗口
            trayIcon.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    client.getClientGUI().setVisible(true); // 还原窗口
                }
            });

            // 添加右键菜单
            PopupMenu popup = new PopupMenu();
            MenuItem exitItem = new MenuItem("Exit");
            exitItem.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    System.exit(0);
                }
            });
            popup.add(exitItem);
            trayIcon.setPopupMenu(popup);

            tray.add(trayIcon);
        }
    }

    public void displayMessage(String caption, String text) {
        if (trayIcon != null) {
            trayIcon.displayMessage(caption, text, TrayIcon.MessageType.INFO);
        }
    }
}

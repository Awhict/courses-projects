package server;

import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.util.HashMap;
import java.util.Map;
import javax.imageio.ImageIO;

public class ServerGUI extends JFrame {
    private JLabel imageLabel;
    private JTree userTree;
    private DefaultMutableTreeNode rootNode;
    private DefaultTreeModel treeModel;
    private Map<String, Boolean> userStatusMap;
    private Map<String, byte[]> userScreenshots;
    private Map<String, Integer> userCaptureIntervals;
    private Map<String, ClientHandler> clientHandlers; // 添加这行
    private String currentUser;
    private JLabel frequencyLabel;
    private JTextField frequencyField;
    private JButton updateFrequencyButton;
    private JTextArea logArea; // 用于显示日志

    public ServerGUI() {
        setTitle("远程屏幕监控系统 - 服务器端");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // 初始化图像标签
        imageLabel = new JLabel();
        add(new JScrollPane(imageLabel), BorderLayout.CENTER);

        // 初始化用户树
        rootNode = new DefaultMutableTreeNode("用户");
        treeModel = new DefaultTreeModel(rootNode);
        userTree = new JTree(treeModel);
        userTree.setCellRenderer(new UserTreeCellRenderer());
        userTree.addTreeSelectionListener(e -> {
            DefaultMutableTreeNode selectedNode = (DefaultMutableTreeNode) userTree.getLastSelectedPathComponent();
            if (selectedNode == null) return;
            Object userObject = selectedNode.getUserObject();
            if (userObject instanceof UserNode) {
                UserNode userNode = (UserNode) userObject;
                currentUser = userNode.getUserName();
                updateImage(userScreenshots.get(currentUser));
                frequencyLabel.setText("截屏频率: " + userCaptureIntervals.getOrDefault(currentUser, 1000) + " ms");
            }
        });
        add(new JScrollPane(userTree), BorderLayout.WEST);

        // 初始化截屏频率显示和修改部分
        JPanel controlPanel = new JPanel();
        frequencyLabel = new JLabel("截屏频率: ");
        frequencyField = new JTextField(5);
        updateFrequencyButton = new JButton("更新频率");
        updateFrequencyButton.addActionListener(e -> {
            try {
                int newFrequency = Integer.parseInt(frequencyField.getText());
                updateClientCaptureInterval(currentUser, newFrequency);
            } catch (NumberFormatException ex) {
                ex.printStackTrace();
            }
        });
        controlPanel.add(frequencyLabel);
        controlPanel.add(frequencyField);
        controlPanel.add(updateFrequencyButton);
        add(controlPanel, BorderLayout.SOUTH);

        // 初始化日志区域
        logArea = new JTextArea();
        logArea.setEditable(false);
        add(new JScrollPane(logArea), BorderLayout.EAST);

        userStatusMap = new HashMap<>();
        userScreenshots = new HashMap<>();
        userCaptureIntervals = new HashMap<>();
        clientHandlers = new HashMap<>(); // 初始化 clientHandlers
        setVisible(true);
    }

    public void updateImage(String userAddress, byte[] imageBytes) {
        userScreenshots.put(userAddress, imageBytes);
        if (userAddress.equals(currentUser)) {
            updateImage(imageBytes);
        }
    }

    public void updateImage(byte[] imageBytes) {
        if (imageBytes == null) return;
        try {
            ByteArrayInputStream bais = new ByteArrayInputStream(imageBytes);
            BufferedImage image = ImageIO.read(bais);
            ImageIcon imageIcon = new ImageIcon(image);
            imageLabel.setIcon(imageIcon);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void updateUserTree(String userName, boolean isOnline) {
        userStatusMap.put(userName, isOnline);
        rootNode.removeAllChildren();
        for (Map.Entry<String, Boolean> entry : userStatusMap.entrySet()) {
            UserNode userNode = new UserNode(entry.getKey(), entry.getValue());
            DefaultMutableTreeNode treeNode = new DefaultMutableTreeNode(userNode);
            rootNode.add(treeNode);
        }
        treeModel.reload();
    }

    public void updateClientCaptureInterval(String userAddress, int newInterval) {
        userCaptureIntervals.put(userAddress, newInterval);
        ClientHandler handler = clientHandlers.get(userAddress);
        if (handler != null) {
            handler.sendCaptureIntervalUpdate(newInterval);
        }
    }

    public void registerClientHandler(String userAddress, ClientHandler handler) {
        clientHandlers.put(userAddress, handler);
    }

    public void log(String message) {
        logArea.append(message + "\n");
    }

    private class UserTreeCellRenderer extends DefaultTreeCellRenderer {
        @Override
        public Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel, boolean expanded, boolean leaf, int row, boolean hasFocus) {
            Component c = super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
            DefaultMutableTreeNode node = (DefaultMutableTreeNode) value;
            Object userObject = node.getUserObject();
            if (userObject instanceof UserNode) {
                UserNode userNode = (UserNode) userObject;
                if (userNode.isOnline()) {
                    setForeground(Color.GREEN);
                } else {
                    setForeground(Color.GRAY);
                }
            }
            return c;
        }
    }

    private class UserNode {
        private String userName;
        private boolean online;

        public UserNode(String userName, boolean online) {
            this.userName = userName;
            this.online = online;
        }

        public String getUserName() {
            return userName;
        }

        public boolean isOnline() {
            return online;
        }

        @Override
        public String toString() {
            return userName;
        }
    }
}

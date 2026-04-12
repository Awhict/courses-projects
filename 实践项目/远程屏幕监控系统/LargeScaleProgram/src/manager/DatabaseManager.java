package manager;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class DatabaseManager {
    private Connection connection;

    public DatabaseManager(String dbURL, String user, String password) throws SQLException {
        this.connection = DriverManager.getConnection(dbURL, user, password);
    }

    public void insertScreenshot(String clientID, byte[] screenshot) throws SQLException {
        String sql = "INSERT INTO screenshots (client_id, screenshot) VALUES (?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, clientID);
            statement.setBytes(2, screenshot);
            statement.executeUpdate();
        }
    }

    public byte[] getScreenshot(String clientID) throws SQLException {
        String sql = "SELECT screenshot FROM screenshots WHERE client_id = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, clientID);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSet.getBytes("screenshot");
                } else {
                    return null;
                }
            }
        }
    }

    public void close() throws SQLException {
        if (connection != null && !connection.isClosed()) {
            connection.close();
        }
    }

    public boolean registerUser(String username, String password, String ip, String mac) throws SQLException {
        String sql = "INSERT INTO users (username, password, ip, mac) VALUES (?, ?, ?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, username);
            statement.setString(2, password);
            statement.setString(3, ip);
            statement.setString(4, mac);
            int rowsInserted = statement.executeUpdate();
            return rowsInserted > 0;
        }
    }

    public boolean loginUser(String username, String password, String ip, String mac) throws SQLException {
        String sql = "SELECT * FROM users WHERE username = ? AND password = ? AND ip = ? AND mac = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, username);
            statement.setString(2, password);
            statement.setString(3, ip);
            statement.setString(4, mac);
            try (ResultSet resultSet = statement.executeQuery()) {
                return resultSet.next();
            }
        }
    }
}

package com.security.crypto.encode;

import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class EncodingUtil {

    // Base64 编码
    public static String encodeBase64(String input) {
        return Base64.getEncoder().encodeToString(input.getBytes(StandardCharsets.UTF_8));
    }

    // Base64 解码
    public static String decodeBase64(String input) {
        byte[] decoded = Base64.getDecoder().decode(input);
        return new String(decoded, StandardCharsets.UTF_8);
    }

    // UTF-8 编码
    public static String encodeUTF8(String input) {
        byte[] bytes = input.getBytes(StandardCharsets.UTF_8);
        return bytesToHex(bytes);
    }

    // UTF-8 解码
    public static String decodeUTF8(String hexInput) {
        byte[] bytes = hexToBytes(hexInput);
        return new String(bytes, StandardCharsets.UTF_8);
    }

    // Unicode 编码
    public static String encodeUnicode(String input) {
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            sb.append(String.format("\\u%04x", (int) c));
        }
        return sb.toString();
    }

    // Unicode 解码
    public static String decodeUnicode(String input) {
        String[] parts = input.split("\\\\u");
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i < parts.length; i++) {
            int code = Integer.parseInt(parts[i], 16);
            sb.append((char) code);
        }
        return sb.toString();
    }

    // 工具：字节数组转十六进制字符串
    private static String bytesToHex(byte[] bytes) {
        StringBuilder hex = new StringBuilder();
        for (byte b : bytes) {
            String h = Integer.toHexString(0xff & b);
            if (h.length() == 1) hex.append('0');
            hex.append(h);
        }
        return hex.toString();
    }

    // 工具：十六进制字符串转字节数组
    private static byte[] hexToBytes(String hex) {
        int len = hex.length();
        byte[] result = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            result[i / 2] = (byte) ((Character.digit(hex.charAt(i), 16) << 4)
                    + Character.digit(hex.charAt(i + 1), 16));
        }
        return result;
    }
}

package com.security.crypto.hash;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import javax.crypto.Mac;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.util.Base64;

public class HashUtil {

    static {
        Security.addProvider(new BouncyCastleProvider());
    }

    // 普通哈希算法
    public static String sha1(String input) throws Exception {
        return hashDigest(input, "SHA-1");
    }

    public static String sha256(String input) throws Exception {
        return hashDigest(input, "SHA-256");
    }

    public static String sha3(String input) throws Exception {
        return hashDigest(input, "SHA3-256");
    }

    public static String ripemd160(String input) throws Exception {
        return hashDigest(input, "RIPEMD160");
    }

    private static String hashDigest(String input, String algorithm) throws Exception {
        MessageDigest digest = MessageDigest.getInstance(algorithm);
        byte[] result = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(result);
    }

    // HMAC 签名
    public static String hmacSHA1(String input, String key) throws Exception {
        return hmacDigest(input, key, "HmacSHA1");
    }

    public static String hmacSHA256(String input, String key) throws Exception {
        return hmacDigest(input, key, "HmacSHA256");
    }

    private static String hmacDigest(String input, String key, String algorithm) throws Exception {
        Mac mac = Mac.getInstance(algorithm);
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), algorithm);
        mac.init(secretKeySpec);
        byte[] result = mac.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(result);
    }

    // PBKDF2 密钥派生
    public static String pbkdf2(String password, String salt) throws Exception {
        int iterations = 10000;
        int keyLength = 256;
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(StandardCharsets.UTF_8), iterations, keyLength);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        byte[] hash = skf.generateSecret(spec).getEncoded();
        return Base64.getEncoder().encodeToString(hash);
    }

    // 工具：字节数组转十六进制
    private static String bytesToHex(byte[] bytes) {
        StringBuilder hex = new StringBuilder();
        for (byte b : bytes) {
            String h = Integer.toHexString(0xff & b);
            if (h.length() == 1) hex.append('0');
            hex.append(h);
        }
        return hex.toString();
    }
}

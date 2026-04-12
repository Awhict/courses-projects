package com.security.crypto.symmetric;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class AESUtil {
    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES/CBC/PKCS5Padding";

    public static String encrypt(String plainText, String key, String iv) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), ALGORITHM);
        IvParameterSpec ivSpec = new IvParameterSpec(Base64.getDecoder().decode(iv));
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivSpec);
        byte[] encrypted = cipher.doFinal(plainText.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public static String decrypt(String cipherText, String key, String iv) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION);
        SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), ALGORITHM);
        IvParameterSpec ivSpec = new IvParameterSpec(Base64.getDecoder().decode(iv));
        cipher.init(Cipher.DECRYPT_MODE, secretKey, ivSpec);
        byte[] decodedBytes = Base64.getDecoder().decode(cipherText);
        byte[] original = cipher.doFinal(decodedBytes);
        return new String(original, StandardCharsets.UTF_8);
    }
}

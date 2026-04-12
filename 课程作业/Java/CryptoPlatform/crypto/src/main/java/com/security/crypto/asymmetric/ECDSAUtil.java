package com.security.crypto.asymmetric;

import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class ECDSAUtil {

    public static KeyPair generateKeyPair() throws Exception {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("EC");
        keyPairGenerator.initialize(256);
        return keyPairGenerator.generateKeyPair();
    }

    public static String sign(String message, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA1withECDSA");
        signature.initSign(privateKey);
        signature.update(message.getBytes());
        return Base64.getEncoder().encodeToString(signature.sign());
    }

    public static boolean verify(String message, String sig, PublicKey publicKey) throws Exception {
        Signature signature = Signature.getInstance("SHA1withECDSA");
        signature.initVerify(publicKey);
        signature.update(message.getBytes());
        return signature.verify(Base64.getDecoder().decode(sig));
    }

    // Base64编码的公钥
    public static PublicKey getBase64PublicKey(String base64PublicKey) throws Exception {
        base64PublicKey = base64PublicKey.replaceAll("\\s+", "");
        byte[] keyBytes = Base64.getDecoder().decode(base64PublicKey);
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("EC");
        return keyFactory.generatePublic(keySpec);
    }

    // Base64编码的私钥
    public static PrivateKey getBase64PrivateKey(String base64PrivateKey) throws Exception {
        base64PrivateKey = base64PrivateKey.replaceAll("\\s+", "");
        byte[] keyBytes = Base64.getDecoder().decode(base64PrivateKey);
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance("EC");
        return keyFactory.generatePrivate(keySpec);
    }
}

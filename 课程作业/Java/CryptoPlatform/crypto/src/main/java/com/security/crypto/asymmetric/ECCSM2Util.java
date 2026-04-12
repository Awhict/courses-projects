package com.security.crypto.asymmetric;

import org.bouncycastle.crypto.params.ParametersWithRandom;
import org.bouncycastle.crypto.util.PrivateKeyFactory;
import org.bouncycastle.crypto.util.PublicKeyFactory;
import org.bouncycastle.crypto.engines.SM2Engine;
import org.bouncycastle.jce.ECNamedCurveTable;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.jce.spec.ECNamedCurveParameterSpec;
import org.bouncycastle.util.encoders.Hex;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class ECCSM2Util {

    private static final String ALGORITHM = "EC";
    private static final String PROVIDER = "BC";

    static {
        if (Security.getProvider(BouncyCastleProvider.PROVIDER_NAME) == null) {
            Security.addProvider(new BouncyCastleProvider());
        }
    }

    // 生成SM2密钥对
    public static KeyPair generateKeyPair() throws Exception {
        ECNamedCurveParameterSpec sm2Spec = ECNamedCurveTable.getParameterSpec("sm2p256v1");
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance(ALGORITHM, PROVIDER);
        keyPairGenerator.initialize(sm2Spec, new SecureRandom());
        return keyPairGenerator.generateKeyPair();
    }

    // 加密
    public static String encrypt(String plaintext, PublicKey publicKey) throws Exception {
        SM2Engine engine = new SM2Engine(SM2Engine.Mode.C1C3C2); // 加密模式

        // 获取 SM2 公钥参数
        org.bouncycastle.crypto.params.AsymmetricKeyParameter pubKey = PublicKeyFactory.createKey(publicKey.getEncoded());

        // 包装为带随机数的参数
        ParametersWithRandom paramWithRandom = new ParametersWithRandom(pubKey, new SecureRandom());

        engine.init(true, paramWithRandom);
        byte[] inputBytes = plaintext.getBytes(StandardCharsets.UTF_8);
        byte[] encryptedBytes = engine.processBlock(inputBytes, 0, inputBytes.length);

        return Hex.toHexString(encryptedBytes);
    }

    // 解密
    public static String decrypt(String ciphertextHex, PrivateKey privateKey) throws Exception {
        byte[] cipherData = Hex.decode(ciphertextHex);
        SM2Engine engine = new SM2Engine(SM2Engine.Mode.C1C3C2); // 匹配加密模式
        org.bouncycastle.crypto.params.AsymmetricKeyParameter privKey = PrivateKeyFactory.createKey(privateKey.getEncoded());
        engine.init(false, privKey);
        byte[] decryptedData = engine.processBlock(cipherData, 0, cipherData.length);
        return new String(decryptedData, StandardCharsets.UTF_8);
    }

    // Base64编码的公钥
    public static PublicKey getBase64PublicKey(String base64PublicKey) throws Exception {
        base64PublicKey = base64PublicKey.replaceAll("\\s+", "");
        byte[] decoded = Base64.getDecoder().decode(base64PublicKey);
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("EC", "BC");
        return keyFactory.generatePublic(keySpec);
    }

    // Base64编码的私钥
    public static PrivateKey getBase64PrivateKey(String base64PrivateKey) throws Exception {
        base64PrivateKey = base64PrivateKey.replaceAll("\\s+", "");
        byte[] decoded = Base64.getDecoder().decode(base64PrivateKey);
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decoded);
        KeyFactory keyFactory = KeyFactory.getInstance("EC", "BC");
        return keyFactory.generatePrivate(keySpec);
    }
}

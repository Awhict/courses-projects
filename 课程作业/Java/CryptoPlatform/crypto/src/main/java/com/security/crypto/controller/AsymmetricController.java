package com.security.crypto.controller;

import com.security.crypto.asymmetric.*;
import org.springframework.web.bind.annotation.*;
import java.security.KeyPair;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.util.Base64;
import java.util.Map;

@RestController
@RequestMapping("/api/asymmetric")
public class AsymmetricController {

    // RSA 生成密钥对
    @GetMapping("/rsa/genkey")
    public Map<String, String> rsaGenKey() throws Exception {
        KeyPair keyPair = RSAUtil.generateKeyPair();
        return Map.of(
                "status", "0",
                "publicKey", Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded()),
                "privateKey", Base64.getEncoder().encodeToString(keyPair.getPrivate().getEncoded())
        );
    }

    // RSA 加密
    @PostMapping("/rsa/encrypt")
    public Map<String, String> rsaEncrypt(@RequestParam("input") String plaintext,
                                          @RequestParam("key") String base64PublicKey) throws Exception {
        PublicKey publicKey = RSAUtil.getBase64PublicKey(base64PublicKey);
        String ciphertext = RSAUtil.encrypt(plaintext, publicKey);
        return Map.of("result", ciphertext, "status", "0");
    }

    // RSA 解密
    @PostMapping("/rsa/decrypt")
    public Map<String, String> rsaDecrypt(@RequestParam("input") String ciphertext,
                                          @RequestParam("key") String base64PrivateKey) throws Exception {
        PrivateKey privateKey = RSAUtil.getBase64PrivateKey(base64PrivateKey);
        String decrypted = RSAUtil.decrypt(ciphertext, privateKey);
        return Map.of("result", decrypted, "status", "0");
    }

    // RSA-SHA1 签名
    @PostMapping("/rsa/sign")
    public Map<String, String> rsaSign(@RequestParam("input") String message,
                                       @RequestParam("key") String base64PrivateKey) throws Exception {
        PrivateKey privateKey = RSAUtil.getBase64PrivateKey(base64PrivateKey);
        String signature = RSASHA1Util.sign(message, privateKey);
        return Map.of("result", signature, "status", "0");
    }

    // RSA-SHA1 验签
    @PostMapping("/rsa/verify")
    public Map<String, String> rsaVerify(@RequestParam("input") String message,
                                         @RequestParam("signature") String signature,
                                         @RequestParam("key") String base64PublicKey) throws Exception {
        PublicKey publicKey = RSAUtil.getBase64PublicKey(base64PublicKey);
        boolean valid = RSASHA1Util.verify(message, signature, publicKey);
        return Map.of("result", String.valueOf(valid), "status", "0");
    }

    // ECC-SM2 生成密钥对
    @GetMapping("/sm2/genkey")
    public Map<String, String> sm2GenKey() throws Exception {
        KeyPair keyPair = ECCSM2Util.generateKeyPair();
        return Map.of(
                "status", "0",
                "publicKey", Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded()),
                "privateKey", Base64.getEncoder().encodeToString(keyPair.getPrivate().getEncoded())
        );
    }

    // ECC-SM2 加密
    @PostMapping("/sm2/encrypt")
    public Map<String, String> sm2Encrypt(@RequestParam("input") String plaintext,
                                          @RequestParam("key") String publicKey) throws Exception {
        PublicKey pubKey = ECCSM2Util.getBase64PublicKey(publicKey);
        String ciphertext = ECCSM2Util.encrypt(plaintext, pubKey);
        return Map.of("result", ciphertext, "status", "0");
    }

    // ECC-SM2 解密
    @PostMapping("/sm2/decrypt")
    public Map<String, String> sm2Decrypt(@RequestParam("input") String ciphertext,
                                          @RequestParam("key") String privateKey) throws Exception {
        PrivateKey priKey = ECCSM2Util.getBase64PrivateKey(privateKey);
        String plaintext = ECCSM2Util.decrypt(ciphertext, priKey);
        return Map.of("result", plaintext, "status", "0");
    }

    // ECDSA 生成密钥对
    @GetMapping("/ecdsa/genkey")
    public Map<String, String> ecdsaGenKey() throws Exception {
        KeyPair keyPair = ECDSAUtil.generateKeyPair();
        return Map.of(
                "status", "0",
                "publicKey", Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded()),
                "privateKey", Base64.getEncoder().encodeToString(keyPair.getPrivate().getEncoded())
        );
    }

    // ECDSA 签名
    @PostMapping("/ecdsa/sign")
    public Map<String, String> ecdsaSign(@RequestParam("input") String message,
                                         @RequestParam("key") String privateKey) throws Exception {
        PrivateKey priKey = ECDSAUtil.getBase64PrivateKey(privateKey);
        String signature = ECDSAUtil.sign(message, priKey);
        return Map.of("result", signature, "status", "0");
    }

    // ECDSA 验签
    @PostMapping("/ecdsa/verify")
    public Map<String, String> ecdsaVerify(@RequestParam("input") String message,
                                           @RequestParam("signature") String signature,
                                           @RequestParam("key") String publicKey) throws Exception {
        PublicKey pubKey = ECDSAUtil.getBase64PublicKey(publicKey);
        boolean valid = ECDSAUtil.verify(message, signature, pubKey);
        return Map.of("result", String.valueOf(valid), "status", "0");
    }
}

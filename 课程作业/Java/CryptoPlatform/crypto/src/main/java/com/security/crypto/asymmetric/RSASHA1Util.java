package com.security.crypto.asymmetric;

import java.security.*;
import java.util.Base64;

public class RSASHA1Util {

    // 签名
    public static String sign(String message, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA1withRSA");
        signature.initSign(privateKey);
        signature.update(message.getBytes());
        return Base64.getEncoder().encodeToString(signature.sign());
    }

    // 验签
    public static boolean verify(String message, String sig, PublicKey publicKey) throws Exception {
        Signature signature = Signature.getInstance("SHA1withRSA");
        signature.initVerify(publicKey);
        signature.update(message.getBytes());
        return signature.verify(Base64.getDecoder().decode(sig));
    }
}

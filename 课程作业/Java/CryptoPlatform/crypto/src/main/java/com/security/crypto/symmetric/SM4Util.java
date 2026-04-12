package com.security.crypto.symmetric;

import org.bouncycastle.crypto.engines.SM4Engine;
import org.bouncycastle.crypto.modes.CBCBlockCipher;
import org.bouncycastle.crypto.paddings.PaddedBufferedBlockCipher;
import org.bouncycastle.crypto.paddings.PKCS7Padding;
import org.bouncycastle.crypto.params.KeyParameter;
import org.bouncycastle.crypto.params.ParametersWithIV;
import java.util.Base64;

public class SM4Util {

    private static final String ENCODING = "UTF-8";

    public static String encrypt(String plainText, byte[] key, byte[] iv) throws Exception {
        PaddedBufferedBlockCipher cipher = new PaddedBufferedBlockCipher(
                new CBCBlockCipher(new SM4Engine()), new PKCS7Padding()
        );
        cipher.init(true, new ParametersWithIV(new KeyParameter(key), iv));

        byte[] input = plainText.getBytes(ENCODING);
        byte[] output = new byte[cipher.getOutputSize(input.length)];
        int length = cipher.processBytes(input, 0, input.length, output, 0);
        length += cipher.doFinal(output, length);

        byte[] encrypted = new byte[length];
        System.arraycopy(output, 0, encrypted, 0, length);
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public static String decrypt(String cipherText, byte[] key, byte[] iv) throws Exception {
        PaddedBufferedBlockCipher cipher = new PaddedBufferedBlockCipher(
                new CBCBlockCipher(new SM4Engine()), new PKCS7Padding()
        );
        cipher.init(false, new ParametersWithIV(new KeyParameter(key), iv));

        byte[] input = Base64.getDecoder().decode(cipherText);
        byte[] output = new byte[cipher.getOutputSize(input.length)];
        int length = cipher.processBytes(input, 0, input.length, output, 0);
        length += cipher.doFinal(output, length);

        return new String(output, 0, length, ENCODING);
    }

    // 支持 Base64 字符串参数的接口

    public static String encryptBase64(String plainText, String base64Key, String base64IV) throws Exception {
        byte[] key = Base64.getDecoder().decode(base64Key);
        byte[] iv = Base64.getDecoder().decode(base64IV);
        return encrypt(plainText, key, iv);
    }

    public static String decryptBase64(String cipherText, String base64Key, String base64IV) throws Exception {
        byte[] key = Base64.getDecoder().decode(base64Key);
        byte[] iv = Base64.getDecoder().decode(base64IV);
        return decrypt(cipherText, key, iv);
    }
}

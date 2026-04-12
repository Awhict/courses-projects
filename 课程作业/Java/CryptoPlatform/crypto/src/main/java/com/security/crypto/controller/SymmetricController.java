package com.security.crypto.controller;

import com.security.crypto.symmetric.AESUtil;
import com.security.crypto.symmetric.RC6Util;
import com.security.crypto.symmetric.SM4Util;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/symmetric")
public class SymmetricController {

    // AES 加密
    @PostMapping("/aes/encrypt")
    public Map<String, Object> encryptAES(@RequestParam String plaintext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String ciphertext = AESUtil.encrypt(plaintext, key, iv);
            response.put("status", 0);
            response.put("result", ciphertext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // AES 解密
    @PostMapping("/aes/decrypt")
    public Map<String, Object> decryptAES(@RequestParam String ciphertext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String plaintext = AESUtil.decrypt(ciphertext, key, iv);
            response.put("status", 0);
            response.put("result", plaintext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // RC6 加密
    @PostMapping("/rc6/encrypt")
    public Map<String, Object> encryptRC6(@RequestParam String plaintext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String ciphertext = RC6Util.encryptBase64(plaintext, key, iv);
            response.put("status", 0);
            response.put("result", ciphertext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // RC6 解密
    @PostMapping("/rc6/decrypt")
    public Map<String, Object> decryptRC6(@RequestParam String ciphertext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String plaintext = RC6Util.decryptBase64(ciphertext, key, iv);
            response.put("status", 0);
            response.put("result", plaintext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // SM4 加密
    @PostMapping("/sm4/encrypt")
    public Map<String, Object> encryptSM4(@RequestParam String plaintext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String ciphertext = SM4Util.encryptBase64(plaintext, key, iv);
            response.put("status", 0);
            response.put("result", ciphertext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // SM4 解密
    @PostMapping("/sm4/decrypt")
    public Map<String, Object> decryptSM4(@RequestParam String ciphertext,
                                          @RequestParam String key,
                                          @RequestParam String iv) {
        Map<String, Object> response = new HashMap<>();
        try {
            String plaintext = SM4Util.decryptBase64(ciphertext, key, iv);
            response.put("status", 0);
            response.put("result", plaintext);
        } catch (Exception e) {
            response.put("status", 1);
            response.put("error", e.getMessage());
        }
        return response;
    }

    // 通用表单处理
    @PostMapping("/process")
    public String process(@RequestParam String algorithm,
                          @RequestParam String operation,
                          @RequestParam String key,
                          @RequestParam String iv,
                          @RequestParam String input,
                          Model model) {
        try {
            String result;
            switch (algorithm.toLowerCase()) {
                case "aes":
                    result = "encrypt".equalsIgnoreCase(operation)
                            ? AESUtil.encrypt(input, key, iv)
                            : AESUtil.decrypt(input, key, iv);
                    break;
                case "rc6":
                    result = "encrypt".equalsIgnoreCase(operation)
                            ? RC6Util.encryptBase64(input, key, iv)
                            : RC6Util.decryptBase64(input, key, iv);
                    break;
                case "sm4":
                    result = "encrypt".equalsIgnoreCase(operation)
                            ? SM4Util.encryptBase64(input, key, iv)
                            : SM4Util.decryptBase64(input, key, iv);
                    break;
                default:
                    throw new IllegalArgumentException("不支持的算法：" + algorithm);
            }
            model.addAttribute("result", result);
        } catch (Exception e) {
            model.addAttribute("result", "错误：" + e.getMessage());
        }
        return "symmetric";
    }
}

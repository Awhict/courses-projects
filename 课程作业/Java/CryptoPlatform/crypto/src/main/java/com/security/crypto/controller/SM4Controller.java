package com.security.crypto.controller;

import com.security.crypto.symmetric.SM4Util;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/sm4")
public class SM4Controller {

    @PostMapping("/encrypt")
    public Map<String, Object> encrypt(@RequestParam String plaintext,
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

    @PostMapping("/decrypt")
    public Map<String, Object> decrypt(@RequestParam String ciphertext,
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

    @PostMapping("/process")
    public String process(@RequestParam String operation,
                          @RequestParam String key,
                          @RequestParam String iv,
                          @RequestParam String input,
                          Model model) {
        try {
            String result;
            if ("encrypt".equalsIgnoreCase(operation)) {
                result = SM4Util.encrypt(input, key.getBytes("UTF-8"), iv.getBytes("UTF-8"));
            } else {
                result = SM4Util.decrypt(input, key.getBytes("UTF-8"), iv.getBytes("UTF-8"));
            }
            model.addAttribute("result", result);
        } catch (Exception e) {
            model.addAttribute("result", "错误：" + e.getMessage());
        }
        return "symmetric";
    }
}

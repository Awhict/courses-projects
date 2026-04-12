package com.security.crypto.controller;

import com.security.crypto.symmetric.RC6Util;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/rc6")
public class RC6Controller {

    @PostMapping("/encrypt")
    public Map<String, Object> encrypt(@RequestParam String plaintext,
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

    @PostMapping("/decrypt")
    public Map<String, Object> decrypt(@RequestParam String ciphertext,
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

    @PostMapping("/process")
    public String process(@RequestParam String operation,
                          @RequestParam String key,
                          @RequestParam String iv,
                          @RequestParam String input,
                          Model model) {
        try {
            String result;
            if ("encrypt".equalsIgnoreCase(operation)) {
                result = RC6Util.encryptBase64(input, key, iv);
            } else {
                result = RC6Util.decryptBase64(input, key, iv);
            }
            model.addAttribute("result", result);
        } catch (Exception e) {
            model.addAttribute("result", "错误：" + e.getMessage());
        }
        return "symmetric";
    }
}

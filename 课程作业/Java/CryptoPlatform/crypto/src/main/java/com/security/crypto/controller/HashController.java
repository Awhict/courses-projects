package com.security.crypto.controller;

import com.security.crypto.hash.HashUtil;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/hash")
public class HashController {

    @PostMapping("/digest")
    public Map<String, Object> digest(@RequestParam String algorithm,
                                      @RequestParam String input,
                                      @RequestParam(required = false) String salt,
                                      @RequestParam(required = false) String key) {
        Map<String, Object> result = new HashMap<>();
        try {
            String hash;
            switch (algorithm.toLowerCase()) {
                case "sha1":
                    hash = HashUtil.sha1(input);
                    break;
                case "sha256":
                    hash = HashUtil.sha256(input);
                    break;
                case "sha3":
                    hash = HashUtil.sha3(input);
                    break;
                case "ripemd160":
                    hash = HashUtil.ripemd160(input);
                    break;
                case "hmacsha1":
                    hash = HashUtil.hmacSHA1(input, key);
                    break;
                case "hmacsha256":
                    hash = HashUtil.hmacSHA256(input, key);
                    break;
                case "pbkdf2":
                    hash = HashUtil.pbkdf2(input, salt);
                    break;
                default:
                    throw new IllegalArgumentException("不支持的算法: " + algorithm);
            }
            result.put("status", 0);
            result.put("result", hash);
        } catch (Exception e) {
            result.put("status", -1);
            result.put("error", e.getMessage());
        }
        return result;
    }
}

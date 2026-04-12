package com.security.crypto.controller;

import com.security.crypto.encode.EncodingUtil;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/encode")
public class EncodingController {

    @PostMapping("/{algorithm}/{operation}")
    public Map<String, Object> process(
            @PathVariable String algorithm,
            @PathVariable String operation,
            @RequestParam String input) {

        Map<String, Object> response = new HashMap<>();
        try {
            String result;
            switch (algorithm.toLowerCase()) {
                case "base64":
                    result = operation.equals("encode") ?
                            EncodingUtil.encodeBase64(input) :
                            EncodingUtil.decodeBase64(input);
                    break;
                case "utf8":
                    result = operation.equals("encode") ?
                            EncodingUtil.encodeUTF8(input) :
                            EncodingUtil.decodeUTF8(input);
                    break;
                case "unicode":
                    result = operation.equals("encode") ?
                            EncodingUtil.encodeUnicode(input) :
                            EncodingUtil.decodeUnicode(input);
                    break;
                default:
                    throw new IllegalArgumentException("不支持的编码算法：" + algorithm);
            }
            response.put("status", 0);
            response.put("result", result);
        } catch (Exception e) {
            response.put("status", -1);
            response.put("error", e.getMessage());
        }
        return response;
    }
}

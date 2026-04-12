package com.security.crypto.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/")
    public String index() {
        return "index"; // 返回 templates/index.html
    }

    @GetMapping("/symmetric")
    public String symmetricPage() {
        return "symmetric"; // 返回 templates/symmetric.html
    }

    @GetMapping("/asymmetric")
    public String asymmetricPage() {
        return "asymmetric"; // 返回 templates/asymmetric.html
    }

    @GetMapping("/hash")
    public String hashPage() {
        return "hash"; // 返回 templates/hash.html
    }

    @GetMapping("/encode")
    public String encodePage() {
        return "encode"; // 返回 templates/encode.html
    }

}

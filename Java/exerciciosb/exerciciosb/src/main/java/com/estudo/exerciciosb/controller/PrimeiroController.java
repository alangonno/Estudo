package com.estudo.exerciciosb.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController()
public class PrimeiroController {


    @GetMapping("/ola")
    public String ola() {
        return "Hello World";
    }
}

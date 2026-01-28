package com.estudo.exerciciosb.controller;

import com.estudo.exerciciosb.models.entidades.Cliente;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("clientes")
public class ClienteController {

    @GetMapping("/qualquer")
    public Cliente getCliente(){
        Cliente cliente = new Cliente(1232, "alan", "83282323");
        return cliente;
    }

//    @GetMapping("/{id}")
//    public Cliente getClienteId(@PathVariable int id) {
//        return new Cliente(id, "neivas", "73492378492374");
//    }
//    @GetMapping
//    public Cliente getClienteId2(@RequestParam(name = "id") int id) {
//        return new Cliente(id, "james", "634535754534923212");
//    }
















    @GetMapping("/{n1}/{n2}")
    public int somar (@PathVariable int n1, @PathVariable int n2) {
        return n1 + n2;
    }

    @GetMapping
    public int subtrair (@RequestParam int a, @RequestParam int b) {
        return a - b;
    }

}

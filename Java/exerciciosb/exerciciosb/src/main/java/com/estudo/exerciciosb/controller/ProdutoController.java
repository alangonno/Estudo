package com.estudo.exerciciosb.controller;


import com.estudo.exerciciosb.models.entidades.Produto;
import com.estudo.exerciciosb.models.entidades.repository.ProdutoRepository;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;

import java.awt.print.Pageable;
import java.sql.ResultSet;
import java.util.List;
import java.util.Optional;
import java.awt.print.Pageable;

@RestController
@RequestMapping("api/produtos")
public class ProdutoController {

    @Autowired
    private ProdutoRepository produtoRepository;

    @PostMapping
    public @ResponseBody Produto novoProduto(@Valid Produto produto) {
        produtoRepository.save(produto);
        return produto;
    }

    @GetMapping
    public List<Produto> obterProdutos() {
        return produtoRepository.findAll();
    }

    @GetMapping("/{id}")
    public Optional<Produto> getById(@PathVariable int id){
         return produtoRepository.findById(id);
    }

    @PutMapping()
    public Produto Update(@Valid Produto produto){
        produtoRepository.save(produto);
        return produto;
    }

    @DeleteMapping("/{id}")
    public void exluirByID(@PathVariable int id) {
        produtoRepository.deleteById(id);
    }

    @GetMapping("/pagina/{numeroPagina}")
    public Page<Produto> getProdutosPaginado(@PathVariable int numeroPagina){
        PageRequest page = PageRequest.of(numeroPagina, 3);
        return produtoRepository.findAll(page);
    }

    @GetMapping("/nome/{nome}")
    public Iterable<Produto> getProdutosByName(@PathVariable String nome){
        return produtoRepository.findByNomeContainingIgnoreCase(nome);
    }


}

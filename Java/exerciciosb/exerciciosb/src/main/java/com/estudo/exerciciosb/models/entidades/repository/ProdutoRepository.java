package com.estudo.exerciciosb.models.entidades.repository;

import com.estudo.exerciciosb.models.entidades.Produto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.ListCrudRepository;

import java.util.Iterator;
import java.util.List;

public interface ProdutoRepository extends JpaRepository<Produto, Integer> {

    public Iterable<Produto> findByNomeContainingIgnoreCase(String parteNome);
}


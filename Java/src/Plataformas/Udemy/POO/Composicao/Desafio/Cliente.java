package POO.Composicao.Desafio;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

public class Cliente {

    final String nome;
    final ArrayList<Compra> listaCompra = new ArrayList<Compra>();

    Cliente(String nome) {
        this.nome = nome;
    }

    void adicionarCompra(Compra compra) {
        this.listaCompra.add(compra);
    }



}

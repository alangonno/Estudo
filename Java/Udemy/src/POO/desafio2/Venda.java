package POO.desafio2;

import java.util.ArrayList;
import java.util.List;

public class Venda {
    Cliente cliente;
    List<ItemVenda> listadeProdutos= new ArrayList();
    double valorTotal = 0;

    void adicionarItem(Produto produto, int quantida) {
        this.listadeProdutos.add(new ItemVenda(produto, quantida));
    }

    void calcularValorTotal() {
        listadeProdutos.forEach(item -> {
            valorTotal += item.produto.preco * item.quantidade;
        });
        System.out.println(valorTotal);

    }

}

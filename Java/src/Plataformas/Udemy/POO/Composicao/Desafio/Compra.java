package POO.Composicao.Desafio;

import java.util.ArrayList;

public class Compra {

    final ArrayList<Item> listaItens = new ArrayList<Item>();

    void adicionarItem(Item item) {
        this.listaItens.add(item);
    }

    double obterValorTotal() {
        if (listaItens.isEmpty()) {
            return 0;
        } else {
            double total = 0;
            for (Item item : listaItens) {
                total += item.produto.preco * item.quant;
            }
        return total;

        }
    }
}

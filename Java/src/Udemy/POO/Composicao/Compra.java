package POO.Composicao;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.List;

public class Compra {

    String cliente;
    ArrayList<Item> itens = new ArrayList<Item>();

    double valorTotal() {
        double total = 0;
        for (Item i : itens) {
            total += i.quant * i.preco;
        }
        return total;
    }
}

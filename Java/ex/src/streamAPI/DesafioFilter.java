package streamAPI;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;

public class DesafioFilter {

    public static void main(String[] args) {

        List<Produto> listaProduto = Arrays.asList(
                new Produto("Carro", 30),
                new Produto("Caneta", 20),
                new Produto("Caderno", 50));
        Predicate<Produto> precomaior = produto -> produto.preco >= 25;
        Predicate<Produto> precomenor = produto -> produto.preco <= 40;
        Function<Produto, String> precobom = produto -> produto.nome + " esta Barato!\n";

        listaProduto.stream().
                filter(precomaior).
                filter(precomenor).
                map(precobom).forEach(System.out::print);
    }
}

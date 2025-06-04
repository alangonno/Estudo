package Lambdas;

import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.function.*;

public class Desafio {

    public static void main(String[] args) {
        Produto p = new Produto("note", 3000, 0.2);
        DecimalFormat dF = new DecimalFormat("0.00");

        Function<Produto, Double>  valorReal =
                prod -> prod.preco * (1 - prod.desconto);

        UnaryOperator<Double> imposto =
                valor -> valor >= 2500 ? valor * (1.085) : valor;

        UnaryOperator<Double> frete =
                valor -> valor >= 3000 ? valor + 100 : valor + 50;

        Function<Double, String> valorFormatado =
                valor -> dF.format(valor); //ou Double.parseDouble(String.format("%.2f", valor);

        Consumer<String> formatarFim =
                valor -> System.out.println("R$" + valor.replace(".", ","));

        //Consumer nao entram em cadeia
        String resultado = valorReal.andThen(imposto).andThen(frete).andThen(valorFormatado).apply(p);
        formatarFim.accept(resultado);

    }


}

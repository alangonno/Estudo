package Lambdas;

public class CalcTeste2 {

    public static void main(String[] args) {

        Calculo soma = (x, y) -> { return x + y; };
        soma  = (x,y) -> x + x + y + y;
        System.out.println(soma.executar(2, 4));
    }
}

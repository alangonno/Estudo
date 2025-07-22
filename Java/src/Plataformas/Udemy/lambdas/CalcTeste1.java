package lambdas;

public class CalcTeste1 {
    public static void main(String[] args) {
        Calculo soma = new Soma();
        Calculo multiplicao = new Multiplicar();

        System.out.println(soma.executar(2, 4));
        System.out.println(multiplicao.executar(2, 4));

        Calculo calculo = new Soma();
        System.out.println(calculo.executar(2, 4));

        calculo = new Multiplicar();
        System.out.println(calculo.executar(2, 4));

    }
}

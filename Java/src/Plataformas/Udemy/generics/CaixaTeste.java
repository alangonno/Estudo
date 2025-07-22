package Plataformas.Udemy.generics;

public class CaixaTeste {

    public static void main(String[] args) {

        Caixa<String> caixaA = new Caixa<>();
        caixaA.guardar("Ola");
        System.out.println(caixaA.abrir());


        Caixa<Double> caixaB = new Caixa<>();
        caixaB.guardar(2.2);
        System.out.println(caixaA.abrir());


    }
}

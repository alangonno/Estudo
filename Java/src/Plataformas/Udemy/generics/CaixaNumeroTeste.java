package Plataformas.Udemy.generics;

public class CaixaNumeroTeste {
    public static void main(String[] args) {
        CaixaNumero<Integer> caixaA = new CaixaNumero<>();
        caixaA.guardar(2);
        System.out.println(caixaA.abrir());

        CaixaNumero<Double> caixaB = new CaixaNumero<>();
        caixaB.guardar(2.2);
        System.out.println(caixaA.abrir());

    }

}

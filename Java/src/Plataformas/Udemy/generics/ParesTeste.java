package Plataformas.Udemy.generics;

public class ParesTeste {

    public static void main(String[] args) {
        Pares<Integer, String> resultado = new Pares<>();

        resultado.adicionar(1, "Maria");
        resultado.adicionar(2, "Alan");
        resultado.adicionar(3, "Pedro");
        resultado.adicionar(1, "Joao");

        System.out.println(resultado.getValor(1));
        System.out.println(resultado.getValor(2));
        System.out.println(resultado.getValor(3));
    }
}

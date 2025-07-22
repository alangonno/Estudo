package Plataformas.Udemy.generics;

public class CaixaObjetoTeste {

    public static void main(String[] args) {
        CaixaObjeto caixaA = new CaixaObjeto();
        caixaA.guardar(2.3);

        Integer coisaA = (Integer) caixaA.abrir();

        CaixaObjeto caixaB = new CaixaObjeto();
        caixaB.guardar("Coisa");

        String coisaB = (String) caixaA.abrir();
        System.out.println(coisaB);


    }


}

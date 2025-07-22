package fundamentos.colecoes;

import java.util.ArrayList;

public class Lista {
   public static void main(String[] args) {
      ArrayList<Usuario> lista = new ArrayList<Usuario>();
      Usuario u1 = new Usuario("alan");

      lista.add(u1);
      lista.add(new Usuario("joao"));
      lista.add(new Usuario("james"));
      lista.add(new Usuario("gomes"));

      System.out.println(lista.get(2)); // Usa o toString para printar
      System.out.println(lista.get(2).nome);

      lista.remove(1);
      lista.remove(new Usuario("alan"));

      for(Usuario u: lista) {
         System.out.println(u.nome);
      }

   }
}

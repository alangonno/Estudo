package fundamentos.colecoes;

import java.util.HashSet;

public class Hash {

    public static void main(String[] args) {
        HashSet<Usuario> usuarios = new HashSet<>();
        usuarios.add(new Usuario("l"));
        usuarios.add(new Usuario("n"));
        usuarios.add(new Usuario("a"));

        boolean resultado = usuarios.contains(new Usuario("l"));
        System.out.println(resultado);


    }


}

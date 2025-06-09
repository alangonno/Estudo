package fundamentos.classe;

public class Equals {

    public static void main(String[] args) {
        Usuario u1 = new Usuario();
        u1.nome = "alan";
        u1.email = "alan@gmail.com";
        Usuario u2 = new Usuario();
        u2.nome = "alan";
        u2.email = "alan@gmail.com";

        System.out.println(u1 == u2);
        System.out.println(u1.equals(u2));
    }
}
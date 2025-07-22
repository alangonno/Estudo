package POO.polimorfismo;

public class Jantar {
    public static void main(String[] args) {
        Pessoa p1 = new Pessoa(60);

        Comida a1 = new Arroz(0.200);
        Comida a2 = new Feijao(0.100);
        Comida a3 = new Sorvete(0.500);

        p1.comer(a1);
        p1.comer(a2);
        p1.comer(a3);
        System.out.println(p1.getPeso());

    }
}

package fundamentos.classe;

public class Jantar {
    public static void main(String[] args) {
        Comida carne = new Comida("carne",1.0);
        Comida arroz = new Comida("arroz", 0.500);
        Comida feijao = new Comida("feijao", 0.200);
        
        Pessoa alan = new Pessoa("alan", 61);
        System.out.printf("%s pesa %.2f KG\n", alan.nome, alan.peso);
        alan.comer(carne);
        alan.comer(arroz);
        alan.comer(feijao);

    }
}

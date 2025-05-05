package fundamentos.classe;

public class Pessoa {
    String nome;
    double peso;

    Pessoa(String nome, double peso) {
        this.nome = nome;
        this.peso = peso;
    }

    void comer(Comida comida) {
        if(comida != null){
            this.peso += comida.peso;
            System.out.printf("%s pesa %.2f KG depois de comer %s que pesa %.2f KG\n", this.nome, this.peso, comida.nome, comida.peso);
        }
    
    }
    
}

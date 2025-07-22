package POO.encapsulamento;

public class Pessoa {

    private int idade = 18;
    private String nome;

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public int getIdade() {
        return idade;
    }

    public void setIdade(int n) {
        this.idade = n;

    }
}

package Plataformas.Udemy.tratamentodeErros.ExceptionPersonalizadaB;

public class StringVaziaException extends Exception {
    String nomeAtributo;

    public StringVaziaException(String nomeAtributo) {
        this.nomeAtributo = nomeAtributo;
    }

    public String getMessage() {
        return String.format("O atributo %s está vazio", nomeAtributo);
    }
}

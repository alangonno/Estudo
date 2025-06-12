package Plataformas.Udemy.tratamentodeErros.ExceptionPersonalizadaA;

public class StringVaziaException extends RuntimeException {
    String nomeAtributo;

    public StringVaziaException(String nomeAtributo) {
        this.nomeAtributo = nomeAtributo;
    }

    public String getMessage() {
        return String.format("O atributo %s está vazio", nomeAtributo);
    }
}

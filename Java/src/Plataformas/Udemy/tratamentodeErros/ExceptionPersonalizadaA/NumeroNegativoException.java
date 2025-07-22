package Plataformas.Udemy.tratamentodeErros.ExceptionPersonalizadaA;

public class NumeroNegativoException extends RuntimeException {
    String nomeAtributo;
    public NumeroNegativoException(String nomeAtributo) {
        this.nomeAtributo = nomeAtributo;
    }

    public String getMessage() {
        return String.format("O atributo %s está negativo", nomeAtributo);
    }
}

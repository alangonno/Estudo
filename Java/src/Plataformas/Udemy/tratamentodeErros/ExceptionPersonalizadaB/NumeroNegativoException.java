package Plataformas.Udemy.tratamentodeErros.ExceptionPersonalizadaB;

public class NumeroNegativoException extends Exception {
    String nomeAtributo;
    public NumeroNegativoException(String nomeAtributo) {
        this.nomeAtributo = nomeAtributo;
    }

    public String getMessage() {
        return String.format("O atributo %s está negativo", nomeAtributo);
    }
}

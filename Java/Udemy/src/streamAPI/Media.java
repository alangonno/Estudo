package streamAPI;

public class Media {

    private double total;
    private double quant;

    public Media adicionar(double valor) {
        total += valor;
        quant++;

        return this;
    }

    public Double getMedia() {
        return total / quant;
    }

    public static Media combinar(Media m1, Media m2) {
        Media resultado = new Media();
        resultado.total = m1.total + m2.total;
        resultado.quant = m1.quant + m2.quant;
        return resultado;
    }
}

package Plataformas.Udemy.generics;

public class CaixaObjeto {

    CaixaObjeto() {
    }

    private Object coisa;

    public void guardar(Object coisa) {
        this.coisa = coisa;
    }

    public Object abrir() {
        return coisa;
    }

}

package Plataformas.Udemy.tratamentodeErros;

public class ChecadaXNaoChecada {
    public static void main(String[] args) {
        geraErro1();


        try {
            geraErro2();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

    }
    //Exceção Nao verificada ou Nao checada
    static void geraErro1() {
        throw new RuntimeException("Erro #1");
    }
    //Exceção checada ou verificada
    static void geraErro2() throws Exception {
        throw  new Exception("Erro #2");
    }
}

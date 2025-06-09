package fundamentos.classe;

public class DataTeste {
    public static void main(String[] args) {
        Data aniversario = new Data(24, 9, 2006);
        Data natal = new Data();
        
        aniversario.imprimirData();
        natal.imprimirData();
    }
}

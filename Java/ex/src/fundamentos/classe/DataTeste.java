package fundamentos.classe;

public class DataTeste {
    public static void main(String[] args) {
        Data aniversario = new Data();
        Data natal = new Data();
        aniversario.dia = 24;
        aniversario.mes = 9;
        aniversario.ano = 2006;

        natal.dia = 25;
        natal.mes = 12;
        natal.ano = 0;

        String natalf = (natal.obterData());
        aniversario.imprimirData();
        natal.imprimirData();
    }
}

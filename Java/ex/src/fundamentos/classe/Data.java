package fundamentos.classe;

public class Data {
    int dia;
    int mes;
    int ano;
    
    String obterData (){
        return String.format("%d/%d/%d\n", dia, mes, ano);
    }
    void imprimirData() {
        System.out.println(obterData());
    }

    Data(){
        dia = 1;
        mes = 1;
        ano = 1970;

    }

    Data(int diaI, int mesI, int anoI){
        dia = diaI;
        mes = mesI;
        ano = anoI;
    }
}

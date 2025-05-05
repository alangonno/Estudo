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
        this(1, 1, 1970);
    }
    Data(int dia, int mes, int ano){
        this.dia = dia;
        this.mes = mes;
        this.ano = ano;
    }
}

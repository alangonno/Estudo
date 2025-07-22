package Plataformas.SantanderBootcamp.cellphone;

public class Main {
    public static void main(String[] args) {
        Cellphone celular = new Cellphone();

        celular.exibirPagina();
        celular.adicionarAba();
        celular.atualizarPag();

        celular.ligar("24999271234");
        celular.atender();
        celular.correioVoz();

        celular.selecionar("Pequenas Alegrias");
        celular.tocar();
        celular.pausar();


    }
}

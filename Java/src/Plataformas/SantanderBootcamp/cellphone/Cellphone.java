package Plataformas.SantanderBootcamp.cellphone;

public class Cellphone implements ReprodutorMusica, Telefone, Navegador{

    @Override
    public void exibirPagina() {
        System.out.println("Exibindo pagina");

    }

    @Override
    public void adicionarAba() {

        System.out.println("adicionando aba");
    }

    @Override
    public void atualizarPag() {

        System.out.println("atualizando pagina");
    }

    @Override
    public void tocar() {
        System.out.println("Tocando");
    }

    @Override
    public void pausar() {
        System.out.println("Pausando ");
    }

    @Override
    public void selecionar(String musica) {

        System.out.println("Selecionando " + musica);
    }

    @Override
    public void atender() {
        System.out.println("Atendendo ");
    }

    @Override
    public void ligar(String numero) {

        System.out.println("Ligando para " + numero);
    }

    @Override
    public void correioVoz() {

        System.out.println("Correio de Voz ativado ");
    }
}

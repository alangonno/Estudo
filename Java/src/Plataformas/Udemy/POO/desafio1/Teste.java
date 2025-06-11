package POO.desafio1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Teste {


    public static void main(String[] args) {
        Conta cc = new ContaCorrente();
        Conta cp = new ContaPoupanca();
        List<Conta> contas = new ArrayList<>();
        contas.add(cc);
        contas.add(cp);

        contas.forEach(conta -> {
            conta.depositar(60);
            conta.sacar(20);
            conta.getSaldo();
        });


    }


}

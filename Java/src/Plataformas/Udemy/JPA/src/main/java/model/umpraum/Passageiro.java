package model.umpraum;

import javax.persistence.*;

@Entity
public class Passageiro {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    private String nome;

    @OneToOne
    private Assento assento;


    public Passageiro() {}

    public Passageiro(String nome, Assento assento) {
        super();
        this.nome = nome;
        this.assento =  assento;
    }

}

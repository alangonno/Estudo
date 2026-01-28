package model.heranca;

import javax.persistence.DiscriminatorValue;
import javax.persistence.Entity;

@Entity
@DiscriminatorValue("AB")
public class AlunoBolsista extends Aluno{

    public AlunoBolsista(Long matricula, String nome, Double bolas) {
        super(matricula, nome);
        this.bolas = bolas;
    }

    private Double bolas;

    public Double getBolas() {
        return bolas;
    }

    public void setBolas(Double bolas) {
        this.bolas = bolas;
    }
}

package teste.basic;

import model.basic.AppUser;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class UpdateUser2 {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpa");
        EntityManager em = emf.createEntityManager();

        em.getTransaction().begin();

        AppUser user = em.find(AppUser.class, 2L);
        em.detach(user); //SEM O DETACH O OBJETO DO CAMPO FICA ATIVO NO CODIGO DA TRANSAÇÂO E É ALTERADO MESMO SEM O MERGE

        user.setName("ALanNL");
        user.setEmail("burubaaaaaaaaaaaaauru");

        em.merge(user);
        em.getTransaction().commit();


        em.close();
        emf.close();
    }
}

package teste.basic;

import model.basic.AppUser;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class NewUser {

    public static void main(String[] args) {

        EntityManagerFactory emf = Persistence
                .createEntityManagerFactory("jpa");
        EntityManager em = emf.createEntityManager();

        AppUser newAppUser = new AppUser("alan", "alannogueira@");

        em.getTransaction().begin();
        em.persist(newAppUser);
        em.getTransaction().commit();

        em.close();
        emf.close();


    }
}

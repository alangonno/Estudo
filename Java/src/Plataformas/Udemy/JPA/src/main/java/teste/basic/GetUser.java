package teste.basic;

import model.basic.AppUser;

import javax.persistence.Entity;
import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class GetUser {

    public static void main(String[] args) {

        EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpa");
        EntityManager em = emf.createEntityManager();

        AppUser user = em.find(AppUser.class, 1L);
        System.out.println(user.getName());

        em.close();
        emf.close();

    }
}

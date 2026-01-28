package teste.basic;

import model.basic.AppUser;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;

public class UpdateUser1 {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpa");
        EntityManager em = emf.createEntityManager();

        em.getTransaction().begin();

        AppUser user = em.find(AppUser.class, 1L);
        user.setName("Gonnon");
        user.setEmail("barabara berebere");

        em.merge(user);

        em.getTransaction().commit();

        em.close();
        emf.close();
    }
}

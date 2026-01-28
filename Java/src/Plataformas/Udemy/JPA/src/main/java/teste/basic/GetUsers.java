package teste.basic;

import model.basic.AppUser;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.TypedQuery;
import java.util.List;

public class GetUsers {
    public static void main(String[] args) {
        EntityManagerFactory emf = Persistence.createEntityManagerFactory("jpa");
        EntityManager em = emf.createEntityManager();

        String jpql = "SELECT u from AppUser u";
        TypedQuery<AppUser> query = em.createQuery(jpql, AppUser.class);
        query.setMaxResults(5);

        List<AppUser> users = query.getResultList();

        for (AppUser user: users) {
            System.out.println(user.getId() + user.getName() + user.getEmail());
        }
        em.close();
        emf.close();
    }
}

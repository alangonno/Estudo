import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Scanner;

public class ExcluirPessoa {
    public static void main(String[] args) throws SQLException{
        
        try(Scanner entrada = new Scanner(System.in)) {
            System.out.println("Digite o id a ser Excluido");
            int id = entrada.nextInt();
            entrada.nextLine();

            String sql = "DELETE FROM pessoas WHERE codigo = ?";

            Connection conexao = FabricaConexao.getConexao();
            PreparedStatement stmt = conexao.prepareStatement(sql);
            stmt.setInt(1, id);
            stmt.execute();

            if(stmt.executeUpdate() > 0) {
                System.out.println("Pessoa excluida");
            } else {
                System.out.println("Não excluido");
            }
            
            stmt.close();
            conexao.close();
        }
        
    }
    
}

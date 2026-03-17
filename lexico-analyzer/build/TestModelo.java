import java.io.*;

public class TestModelo {
    public static void main(String[] args) throws Exception {
        // Dados de teste
        Modelo lexer = new Modelo(new FileReader("../test/modelo.rtf"));
        lexer.setNome("Cassio Jones Dhein");
        lexer.setData("16 de marco de 2026");
        lexer.setValor(15000.00);
        lexer.setNumeroParcelas(24);
        lexer.setJurosMensal(1.5);
        
        System.out.println("=== CONTRATO GERADO ===");
        System.out.println("");
        
        while (lexer.yylex() != Modelo.YYEOF) {
            // Continua lendo
        }
    }
}

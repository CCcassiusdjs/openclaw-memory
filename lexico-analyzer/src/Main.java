import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Uso: java Main <arquivo>");
            System.out.println("     java Main --test    (usa codigo de exemplo)");
            System.exit(1);
        }
        
        if (args[0].equals("--test")) {
            String testCode = "// Exemplo de codigo\n" +
                "int contador = 0;\n" +
                "float pi = 3.14159;\n" +
                "string mensagem = \"Ola, Mundo!\";\n" +
                "bool ativo = true;\n" +
                "func main() {\n" +
                "    int x = 10;\n" +
                "    float y = 20.5;\n" +
                "    if (x < y) {\n" +
                "        contador++;\n" +
                "        return x + y;\n" +
                "    } else {\n" +
                "        contador--;\n" +
                "        return 0;\n" +
                "    }\n" +
                "    while (contador < 100) {\n" +
                "        contador += 1;\n" +
                "    }\n" +
                "    int[] nums = [1, 2, 3, 4, 5];\n" +
                "}\n";
            
            System.out.println("=== CODIGO DE ENTRADA ===");
            System.out.println(testCode);
            System.out.println("=== ANALISE LEXICA ===\n");
            
            Lexer lexer = new Lexer(new StringReader(testCode));
            while (lexer.yylex() != Lexer.YYEOF) {
                // Continua lendo
            }
            System.out.println("\n✅ Analise lexica concluida!");
        } else {
            FileReader reader = new FileReader(args[0]);
            Lexer lexer = new Lexer(reader);
            while (lexer.yylex() != Lexer.YYEOF) {
                // Continua lendo
            }
            System.out.println("\n✅ Analise lexica concluida!");
        }
    }
}
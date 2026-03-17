import java.io.*;

public class MainPath {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Uso: java MainPath <arquivo>");
            System.out.println("     java MainPath --test    (usa exemplos)");
            System.exit(1);
        }
        
        if (args[0].equals("--test")) {
            String testPaths = "D:\\acad\\disc\\compil\\compil_u02_lexico\n" +
                "ExercicioLexico.doc\n" +
                "\\Windows\\System32\n" +
                "C:\\Users\\test\\file.txt\n" +
                "arquivo_sem_path.txt\n" +
                "D:\\path\\com\\espaços\\file\n" +
                "/unix/path/file.txt\n" +
                "C:file.txt\n";
            
            System.out.println("=== ENTRADAS DE TESTE ===");
            System.out.println(testPaths);
            System.out.println("=== ANALISE ===\n");
            
            PathFileName lexer = new PathFileName(new StringReader(testPaths));
            while (lexer.yylex() != PathFileName.YYEOF) {
                // Continua lendo
            }
        } else {
            FileReader reader = new FileReader(args[0]);
            PathFileName lexer = new PathFileName(reader);
            while (lexer.yylex() != PathFileName.YYEOF) {
                // Continua lendo
            }
        }
    }
}

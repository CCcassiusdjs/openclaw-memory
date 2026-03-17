%%

%class Lexer
%unicode
%int
%line
%column
%standalone

%{
    private int tokenCount = 0;
    private int errorCount = 0;
    
    public String getPosition() {
        return "L" + (yyline + 1) + ":C" + (yycolumn + 1);
    }
    
    private void printToken(String type, String value) {
        tokenCount++;
        System.out.printf("[%-12s] %s = \"%s\"%n", type, getPosition(), value);
    }
    
    public void printStats() {
        System.out.println("");
        System.out.println("=== ESTATISTICAS DO LEXER ===");
        System.out.println("Tokens reconhecidos: " + tokenCount);
        System.out.println("Erros lexicos: " + errorCount);
        System.out.println("Linhas processadas: " + (yyline + 1));
    }
%}

DIGITO = [0-9]
LETRA = [a-zA-Z_]
LETRA_DIGITO = {LETRA}|{DIGITO}

INTEIRO = {DIGITO}+
DECIMAL = {DIGITO}+ "." {DIGITO}+
NUMERO = ({INTEIRO}|{DECIMAL}) ([eE][+-]?{DIGITO}+)?

IDENT = {LETRA} {LETRA_DIGITO}*

STRING = \" ([^\"]|\\\"|\\\\)* \"  |  \' ([^\']|\\\'|\\\\)* \'

COMENTARIO_LINHA = "//" [^\n]*
COMENTARIO_BLOCO = "/*" [^*]* "*" ([^/][^*]* "*")* "/"

ESPACO = [ \t\n\r]+

OP_RELACIONAL = "=="|"!="|"<"|">"|"<="|">="
OP_LOGICO = "&&"|"||"
OP_ATRIBUICAO = "="|"+="|"-="|"*="|"/="
OP_ARITMETICO = "+"|"-"|"*"|"/"|"%"|"\\"|"^"
OP_INCREMENTO = "++"|"--"

DELIMITADOR = ";"|":"|","|"."|"("|")"|"{"|"}"|"["|"]"

KEYWORD = "int"|"float"|"string"|"bool"|"void"|
           "if"|"else"|"elif"|"while"|"for"|"return"|
           "func"|"class"|"struct"|"import"|"export"|
           "true"|"false"|"null"|"const"|"var"|"let"|
           "break"|"continue"|"switch"|"case"|"default"

%%

{COMENTARIO_LINHA} { printToken("COMMENT", yytext()); }
{COMENTARIO_BLOCO} { printToken("COMMENT_BLOCK", yytext()); }

{KEYWORD} { printToken("KEYWORD", yytext()); }
{IDENT} { printToken("IDENT", yytext()); }
{INTEIRO} { printToken("INT", yytext()); }
{DECIMAL} { printToken("FLOAT", yytext()); }
{NUMERO} { printToken("NUMBER", yytext()); }

{STRING} {
    String text = yytext();
    String content = text.substring(1, text.length() - 1);
    content = content.replace("\\\"", "\"")
                     .replace("\\'", "'")
                     .replace("\\\\", "\\")
                     .replace("\\n", "\n")
                     .replace("\\t", "\t");
    printToken("STRING", content);
}

{OP_RELACIONAL} { printToken("OP_REL", yytext()); }
{OP_LOGICO} { printToken("OP_LOGIC", yytext()); }
{OP_ATRIBUICAO} { printToken("OP_ASSIGN", yytext()); }
{OP_ARITMETICO} { printToken("OP_ARITH", yytext()); }
{OP_INCREMENTO} { printToken("OP_INC", yytext()); }

{DELIMITADOR} {
    String delim = yytext();
    String type;
    if (delim.equals("(")) type = "LPAREN";
    else if (delim.equals(")")) type = "RPAREN";
    else if (delim.equals("{")) type = "LBRACE";
    else if (delim.equals("}")) type = "RBRACE";
    else if (delim.equals("[")) type = "LBRACKET";
    else if (delim.equals("]")) type = "RBRACKET";
    else if (delim.equals(";")) type = "SEMICOLON";
    else if (delim.equals(":")) type = "COLON";
    else if (delim.equals(",")) type = "COMMA";
    else if (delim.equals(".")) type = "DOT";
    else type = "DELIM";
    printToken(type, delim);
}

{ESPACO} { }

. {
    errorCount++;
    System.out.printf("[ERRO LEXICO] %s: Caractere invalido '%s'%n", getPosition(), yytext());
}

<<EOF>> {
    printStats();
    return YYEOF;
}
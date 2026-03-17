/* Scanner JFlex Completo - Linguagem de Programação Simples */

%%

// Seção de Declarações
%class Scanner
%unicode
%int
%line
%column
%standalone

%{
  static int numNumeros = 0;
  static int numIdentificadores = 0;
  static int numOperadores = 0;
  static int numKeywords = 0;
  static int numDelimitadores = 0;
  static int numErros = 0;
%}

// Macros
DIGITO = [0-9]
LETRA = [a-zA-Z_]
NUMERO = {DIGITO}+ ("." {DIGITO}+)?
IDENT = {LETRA} ({LETRA}|{DIGITO})*
OPERADOR = [\+\-\*/=<>!&|]+
DELIMITADOR = [;:,\.\(\)\{\}\[\]]
ESPACO = [ \t\n\r]+

// Keywords
KEYWORD = "if"|"else"|"while"|"for"|"int"|"float"|"return"|"void"|"break"|"continue"|"true"|"false"

%%

// Seção de Regras

{KEYWORD} {
  System.out.println("KEYWORD: " + yytext() + " (linha " + (yyline+1) + ")");
  numKeywords++;
}

{NUMERO} {
  System.out.println("NUMBER: " + yytext() + " (linha " + (yyline+1) + ")");
  numNumeros++;
}

{IDENT} {
  System.out.println("IDENT: " + yytext() + " (linha " + (yyline+1) + ")");
  numIdentificadores++;
}

{OPERADOR} {
  System.out.println("OPERATOR: " + yytext() + " (linha " + (yyline+1) + ")");
  numOperadores++;
}

{DELIMITADOR} {
  System.out.println("DELIM: " + yytext() + " (linha " + (yyline+1) + ")");
  numDelimitadores++;
}

{ESPACO} {
  // Ignorar espaços em branco
}

. {
  System.out.println("ERROR: Caractere inválido '" + yytext() + "' (linha " + (yyline+1) + ")");
  numErros++;
}

<<EOF>> {
  System.out.println("\n=== RELATÓRIO ===");
  System.out.println("Keywords: " + numKeywords);
  System.out.println("Numbers: " + numNumeros);
  System.out.println("Identifiers: " + numIdentificadores);
  System.out.println("Operators: " + numOperadores);
  System.out.println("Delimiters: " + numDelimitadores);
  System.out.println("Errors: " + numErros);
  System.out.println("Total tokens: " + (numKeywords + numNumeros + numIdentificadores + numOperadores + numDelimitadores + numErros));
  return YYEOF;
}
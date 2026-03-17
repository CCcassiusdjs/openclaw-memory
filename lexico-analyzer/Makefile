# Makefile para Analisador Léxico

# Variáveis
JFLEX = jflex
JAVAC = javac
JAVA = java

# Diretórios
SRC_DIR = src
BUILD_DIR = build
TEST_DIR = test

# Arquivos
FLEX_FILE = $(SRC_DIR)/Lexer.flex
JAVA_FILE = $(BUILD_DIR)/Lexer.java
CLASS_FILES = $(BUILD_DIR)/Lexer.class $(BUILD_DIR)/Token.class $(BUILD_DIR)/TokenType.class $(BUILD_DIR)/Main.class

# Opções
JFLEX_FLAGS = --verbose
JAVAC_FLAGS = -d $(BUILD_DIR)

.PHONY: all clean test run

# Alvo padrão
all: $(CLASS_FILES)

# Criar diretório de build
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Gerar Java a partir do Flex
$(JAVA_FILE): $(FLEX_FILE) | $(BUILD_DIR)
	$(JFLEX) $(JFLEX_FLAGS) -d $(BUILD_DIR) $(FLEX_FILE)

# Compilar classes Java
$(BUILD_DIR)/Lexer.class: $(JAVA_FILE) | $(BUILD_DIR)
	$(JAVAC) $(JAVAC_FLAGS) $(BUILD_DIR)/Lexer.java

$(BUILD_DIR)/TokenType.class: $(BUILD_DIR)/Lexer.class
	$(JAVAC) $(JAVAC_FLAGS) $(BUILD_DIR)/TokenType.java

$(BUILD_DIR)/Token.class: $(BUILD_DIR)/TokenType.class
	$(JAVAC) $(JAVAC_FLAGS) $(BUILD_DIR)/Token.java

$(BUILD_DIR)/Main.class: $(BUILD_DIR)/Token.class
	$(JAVAC) $(JAVAC_FLAGS) $(BUILD_DIR)/Main.java

# Executar com arquivo de teste
test: all
	cd $(BUILD_DIR) && $(JAVA) Main --test

# Executar com arquivo fornecido
run: all
	@if [ -z "$(FILE)" ]; then \
		echo "Uso: make run FILE=arquivo.txt"; \
		exit 1; \
	fi
	cd $(BUILD_DIR) && $(JAVA) Main ../$(FILE)

# Executar com código inline
inline: all
	@echo "Digite o código (Ctrl+D para terminar):"
	cd $(BUILD_DIR) && $(JAVA) Main /dev/stdin

# Limpar arquivos gerados
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(SRC_DIR)/*.class $(SRC_DIR)/*.java~

# Ajuda
help:
	@echo "=== Analisador Léxico - Comandos ==="
	@echo "make          - Compila o analisador"
	@echo "make test     - Executa com código de teste"
	@echo "make run FILE=arquivo.txt - Analisa um arquivo"
	@echo "make clean    - Remove arquivos gerados"
	@echo "make help     - Mostra esta ajuda"
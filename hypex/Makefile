# Makefile for HypEx - Hyperbolic File Explorer
# 
# Build: make
# Clean: make clean
# Install: make install
# Debug: make debug

CC = gcc
CFLAGS = -Wall -Wextra -Werror -O3 -fPIC -std=c11
CFLAGS_DEBUG = -Wall -Wextra -g -O0 -fPIC -std=c11 -DDEBUG
LDFLAGS = -lm -lpthread -lsqlite3

# OpenGL dependencies (platform-specific)
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LDFLAGS += -lglfw -lGL -lGLU
    CFLAGS += $(shell pkg-config --cflags glfw3 gl)
    LDFLAGS += $(shell pkg-config --libs glfw3 gl)
endif
ifeq ($(UNAME_S),Darwin)
    LDFLAGS += -framework OpenGL -framework Cocoa -framework IOKit
    CFLAGS += -I/usr/local/include
    LDFLAGS += -L/usr/local/lib -lglfw
endif

# Directories
SRCDIR = src
BUILDDIR = build
BINDIR = bin
SHADERDIR = shaders

# Source files
SRCS = $(wildcard $(SRCDIR)/*.c)
OBJS = $(SRCS:$(SRCDIR)/%.c=$(BUILDDIR)/%.o)
DEPS = $(SRCS:$(SRCDIR)/%.c=$(BUILDDIR)/%.d)

# Target
TARGET = $(BINDIR)/hypex

# Default target
all: dirs $(TARGET)

# Create directories
dirs:
	@mkdir -p $(BUILDDIR) $(BINDIR)

# Link
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
	@echo "Built $(TARGET)"

# Compile
$(BUILDDIR)/%.o: $(SRCDIR)/%.c $(SRCDIR)/hyperbolic.h
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

# Debug build
debug: CFLAGS := $(CFLAGS_DEBUG)
debug: clean all
	@echo "Debug build complete"

# Run with default path
run: $(TARGET)
	./$(TARGET) --root /home/$(USER)

# Run with specific path
run-custom: $(TARGET)
	@read -p "Enter root path: " path; \
	./$(TARGET) --root "$$path"

# Install dependencies (Fedora/RHEL)
install-deps-fedora:
	sudo dnf install -y glfw-devel mesa-libGL-devel mesa-libGLU-devel sqlite-devel

# Install dependencies (Ubuntu/Debian)
install-deps-ubuntu:
	sudo apt install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev libsqlite3-dev

# Install dependencies (macOS)
install-deps-macos:
	brew install glfw sqlite3

# Install system-wide
install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/hypex
	@echo "Installed to /usr/local/bin/hypex"

# Uninstall
uninstall:
	rm -f /usr/local/bin/hypex
	@echo "Uninstalled hypex"

# Clean build artifacts
clean:
	rm -rf $(BUILDDIR) $(BINDIR)
	find . -name "*.d" -delete
	find . -name "*.o" -delete

# Deep clean (including generated files)
distclean: clean
	rm -rf logs/*.log
	rm -rf data/*.db

# Run tests
test: $(TARGET)
	@echo "Running tests..."
	./$(TARGET) --test

# Format code
format:
	find $(SRCDIR) -name "*.c" -o -name "*.h" | xargs clang-format -i

# Static analysis
analyze:
	cppcheck --enable=all --std=c11 $(SRCDIR)

# Memory check (requires valgrind)
memcheck: $(TARGET)
	valgrind --leak-check=full --show-leak-kinds=all ./$(TARGET) --root /tmp

# Generate documentation
docs:
	doxygen Doxyfile

# Include dependency files
-include $(DEPS)

# Phony targets
.PHONY: all dirs clean distclean debug run run-custom install uninstall test format analyze memcheck docs install-deps-fedora install-deps-ubuntu install-deps-macos

# Help
help:
	@echo "HypEx - Hyperbolic File Explorer"
	@echo ""
	@echo "Targets:"
	@echo "  all          - Build the project (default)"
	@echo "  clean        - Remove build artifacts"
	@echo "  debug        - Build with debug symbols"
	@echo "  run          - Run with default root path"
	@echo "  run-custom   - Run with custom root path"
	@echo "  install      - Install system-wide"
	@echo "  test         - Run tests"
	@echo "  format       - Format code with clang-format"
	@echo "  analyze      - Static analysis with cppcheck"
	@echo "  memcheck     - Memory check with valgrind"
	@echo ""
	@echo "Install dependencies:"
	@echo "  install-deps-fedora  - Install on Fedora/RHEL"
	@echo "  install-deps-ubuntu  - Install on Ubuntu/Debian"
	@echo "  install-deps-macos   - Install on macOS"
	@echo ""
	@echo "Usage: hypex --root /path/to/root"
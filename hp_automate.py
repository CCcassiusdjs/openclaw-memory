#!/usr/bin/env python3
"""
Script para automação de teclado/mouse e conexão serial ao switch HP
"""

import evdev
from evdev import UInput, ecodes as e, list_devices
import subprocess
import time
import sys

def type_text(text, delay=0.1):
    """Digita texto simulando teclado"""
    ui = UInput()
    
    char_map = {
        'a': e.KEY_A, 'b': e.KEY_B, 'c': e.KEY_C, 'd': e.KEY_D,
        'e': e.KEY_E, 'f': e.KEY_F, 'g': e.KEY_G, 'h': e.KEY_H,
        'i': e.KEY_I, 'j': e.KEY_J, 'k': e.KEY_K, 'l': e.KEY_L,
        'm': e.KEY_M, 'n': e.KEY_N, 'o': e.KEY_O, 'p': e.KEY_P,
        'q': e.KEY_Q, 'r': e.KEY_R, 's': e.KEY_S, 't': e.KEY_T,
        'u': e.KEY_U, 'v': e.KEY_V, 'w': e.KEY_W, 'x': e.KEY_X,
        'y': e.KEY_Y, 'z': e.KEY_Z,
        '0': e.KEY_0, '1': e.KEY_1, '2': e.KEY_2, '3': e.KEY_3,
        '4': e.KEY_4, '5': e.KEY_5, '6': e.KEY_6, '7': e.KEY_7,
        '8': e.KEY_8, '9': e.KEY_9,
        ' ': e.KEY_SPACE, '-': e.KEY_MINUS, '=': e.KEY_EQUAL,
        '_': e.KEY_MINUS, '+': e.KEY_EQUAL,
        '\n': e.KEY_ENTER,
    }
    
    for char in text.lower():
        if char in char_map:
            ui.write(e.EV_KEY, char_map[char], 1)
            ui.syn()
            time.sleep(0.05)
            ui.write(e.EV_KEY, char_map[char], 0)
            ui.syn()
            time.sleep(delay)
    
    del ui

def open_terminal():
    """Abre um terminal"""
    # Tenta abrir terminal no RHEL (tilix ou gnome-terminal)
    try:
        subprocess.Popen(['tilix'])
    except FileNotFoundError:
        try:
            subprocess.Popen(['gnome-terminal'])
        except FileNotFoundError:
            subprocess.Popen(['xterm'])
    time.sleep(2)

def main():
    print("=== Automação Switch HP V1910 ===")
    print("1. Abrindo terminal...")
    
    # Abre terminal
    open_terminal()
    
    print("2. Aguardando 3 segundos...")
    time.sleep(3)
    
    print("3. Digitando comando picocom...")
    # Digita: picocom -b 38400 /dev/ttyUSB0
    type_text("picocom -b 38400 /dev/ttyUSB0\n", delay=0.15)
    
    print("4. Aguardando conexão (5 segundos)...")
    time.sleep(5)
    
    print("5. Enviando credenciais e comandos...")
    # Login
    type_text("admin\n", delay=0.5)
    time.sleep(1)
    
    # Senha
    type_text("admin\n", delay=0.5)
    time.sleep(2)
    
    # Comando cmdline-mode
    type_text("_cmdline-mode on\n", delay=0.3)
    time.sleep(1)
    
    # Confirmação
    type_text("y\n", delay=0.5)
    time.sleep(1)
    
    # Código
    type_text("512900\n", delay=0.3)
    
    print("\n=== Comandos enviados! ===")
    print("O terminal deve estar conectado ao switch.")
    print("Use Ctrl+A, Ctrl+X para sair do picocom")

if __name__ == "__main__":
    main()

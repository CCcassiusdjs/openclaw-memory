name: moodle-access
description: Acessar Moodle PUCRS e buscar disciplina Desenvolvimento de Jogos
args:
  browser:
    type: string
    default: firefox
    description: Navegador a usar (firefox/chrome)
  url:
    type: string
    default: https://moodle.pucrs.br/
    description: URL do Moodle
steps:
  - id: check_firefox
    command: which firefox
    description: Verificar se Firefox está instalado
  - id: close_chromium
    command: pkill -f chromium || true
    description: Fechar Chromium se aberto
  - id: open_firefox
    command: firefox --new-window "https://moodle.pucrs.br/" &
    description: Abrir Firefox com Moodle
    approval: false
# Veredito Técnico: Viabilidade de Reconstrução de Simulação 3D

## Análise Técnica dos Dados Disponíveis para Reconstrução Visual de Cenários de Falha

---

## 1. Resumo Executivo

**Conclusão: NÃO é viável reconstruir uma simulação 3D fidedigna da trajetória do drone com os dados disponíveis.**

É possível criar uma **animação ilustrativa** baseada em premissas simplificadoras, mas não uma **reconstrução precisa** do que aconteceu em cada execução.

---

## 2. Dados Disponíveis

### 2.1 Groundtruth (Dados de Entrada)

| Dado | Fonte | Conteúdo | Qualidade |
|------|-------|----------|-----------|
| **GPS** | `gps.csv` | Posição fixa (lat, lng, alt) | ✅ Completo |
| **Baro** | `baro.csv` | Altitude barométrica | ✅ Completo |
| **IMU** | `imu.csv` | Acelerômetro, giroscópio | ✅ Completo |
| **Mag** | `mag.csv` | Campo magnético | ✅ Completo |
| **PWM** | `pwm.csv` | Sinais de controle | ✅ Completo |

**Características do Groundtruth:**
- Duração: ~10 segundos
- Cenário: Hover estático (drone parado no ar)
- Posição: Fixa (lat=-30.034647, lng=-51.217658, alt=100m GPS / ~10m baro)
- Sensores: Funcionando corretamente (sem ruído injetado)

### 2.2 Output Vector (Resultado)

| Campo | Tipo | Conteúdo | Útil para simulação? |
|-------|------|----------|---------------------|
| `ekf_flags` | uint32 | Status bitmask | ⚠️ Indica quais sensores completaram |
| `armed_successfully` | uint32 | Flag de arming | ⚠️ Indica se armou |
| `total_gps_drops` | uint32 | Contador GPS | ⚠️ Indica perda de GPS |
| `pos_error_ned_m[3]` | float[3] | **Status flags, NÃO posição** | ❌ Não contém posição |
| `att_error_rpy_deg[3]` | float[3] | **Status flags, NÃO atitude** | ❌ Não contém atitude |

**Importante:** Os campos `pos_error_ned_m` e `att_error_rpy_deg` NÃO contêm a posição ou atitude estimada. Eles são flags de status que indicam se houve erro ou sucesso em cada sensor.

### 2.3 Runtime Log

O log `arducopter_runtime.log` contém apenas mensagens de inicialização e status do emulador:
- Timestamps de inicialização dos sensores
- Status de replay dos datasets
- Timing summary

**Não contém:**
- Estados do EKF
- Trajetória estimada
- Variáveis internas

---

## 3. Dados Necessários para Simulação 3D Fidedigna

### 3.1 Para reconstruir a trajetória do drone:

| Dado | Necessário para | Disponível? |
|------|-----------------|-------------|
| **Posição NED estimada** | Mostrar trajetória 3D | ❌ Não |
| **Velocidade NED estimada** | Mostrar velocidade | ❌ Não |
| **Atitude (quaternions)** | Mostrar orientação | ❌ Não |
| **Bias do giroscópio** | Correção de deriva | ❌ Não |
| **Covariância do estado** | Incerteza da estimativa | ❌ Não |
| **Comandos de controle** | Mostrar ações do piloto | ⚠️ PWM disponível |
| **Timestamps de falha** | Sincronizar animação | ❌ Não |

### 3.2 Para mostrar o momento da falha:

| Dado | Necessário para | Disponível? |
|------|-----------------|-------------|
| **Endereço do bit flip** | Localizar onde errou | ❌ Não |
| **Registro do processador** | Estado no momento da falha | ❌ Não |
| **Stack trace** | Onde o código travou | ❌ Não |
| **Tempo exato da falha** | Sincronizar animação | ❌ Não |

---

## 4. Análise Detalhada

### 4.1 O Output Vector NÃO Contém Estado

A estrutura `output_vector_type` foi projetada para **classificação de falhas**, não para reconstrução de trajetória:

```c
// O que está no output vector:
pos_error_ned_m[0] = 1.0;  // Status flag: "GPS OK" ou "GPS FAILED"
pos_error_ned_m[1] = 1.0;  // Status flag: "IMU OK" ou "IMU FAILED"
pos_error_ned_m[2] = 1.0;  // Status flag: "BARO OK" ou "BARO FAILED"
att_error_rpy_deg[0] = 1.0; // Status flag: "ROLL OK" ou "ROLL FAILED"
att_error_rpy_deg[1] = 1.0; // Status flag: "PITCH OK" ou "PITCH FAILED"
att_error_rpy_deg[2] = 0.0; // Status flag: "YAW OK" ou "YAW FAILED"

// O que seria necessário para reconstrução:
// pos_ned_m[0] = 0.5;    // Posição North em metros
// pos_ned_m[1] = -0.3;   // Posição East em metros
// pos_ned_m[2] = 10.0;   // Posição Down em metros
// vel_ned_mps[0] = 0.1;   // Velocidade North m/s
// vel_ned_mps[1] = 0.0;  // Velocidade East m/s
// vel_ned_mps[2] = 0.0;  // Velocidade Down m/s
// quaternion[0-3] = ...; // Orientação
```

### 4.2 O Groundtruth é Estático

Os dados de entrada representam um **hover estático**:
- Drone em posição fixa
- Velocidade zero
- Altitude constante (~10m)

**Implicação:** Mesmo que tivéssemos a trajetória estimada, ela seria aproximadamente:
- Posição: constante
- Velocidade: zero
- Atitude: neutra (level)

### 4.3 Não há Traceback da Falha

O output vector indica **quais sensores completaram**, mas não:
- Quando ocorreu a falha (timestamp)
- Onde no código (endereço de memória)
- Qual foi o bit flip (posição exata)
- Como o estado interno foi afetado

### 4.4 O Logger está Desabilitado

O parâmetro `LOG_BACKEND_TYPE 0` desabilita o logger interno do ArduCopter. Isso significa que **não há gravação de**:
- Estados do EKF
- Mensagens MAVLink
- Telemetria de voo
- Variáveis internas

---

## 5. O Que É Possível Fazer

### 5.1 Animação Ilustrativa (Não Fidedigna)

Com premissas simplificadoras, é possível criar uma animação que **ilustra** o conceito:

| Elemento | Fonte | Premissa |
|----------|-------|----------|
| Posição inicial | Groundtruth GPS | Fixa (hover) |
| Altitude inicial | Groundtruth baro | ~10m |
| Queda | Física teórica | Queda livre |
| Momento da falha | Flags | Aproximado (assumir início do teste) |
| Tipo de falha | Output vector | Classificação A-E |

**Limitações:**
- Não mostra a trajetória real do drone
- Não mostra a atitude real (roll/pitch/yaw)
- Não mostra quando exatamente a falha ocorreu
- Não mostra qual sensor falhou primeiro
- Não mostra como o EKF reagiu à falha

### 5.2 Classificação Estatística

É possível classificar as falhas e mostrar distribuições:

```
Type A (Immediate crash): 69.0% - Nenhum sensor completou
Type B (GPS failed):        13.8% - GPS falhou, outros OK
Type C (Attitude failed):   17.2% - Apenas GPS completou
```

### 5.3 Física da Queda

Com a altura inicial (~10m), é possível calcular:
- Tempo de queda: ~1.43s
- Velocidade de impacto: ~14 m/s (50 km/h)
- Energia de impacto: ~151 J

---

## 6. Justificativa Técnica

### 6.1 Por que não é possível reconstruir

A reconstrução de trajetória requer **dados temporais do estado estimado**. O sistema de testes foi projetado para **classificar falhas**, não para **registrar trajetória**.

**Analogia:** É como ter o resultado de um teste médico (positivo/negativo) sem ter os dados do exame (imagens, valores). Você sabe que houve falha, mas não tem os dados para visualizar o que aconteceu.

### 6.2 O que seria necessário para reconstrução

Para uma reconstrução completa, o sistema precisaria gravar:

```c
// Dados necessários (NÃO disponíveis):
struct trajectory_record {
    uint64_t timestamp_ms;
    float position_ned_m[3];      // Posição estimada
    float velocity_ned_mps[3];    // Velocidade estimada
    float attitude_quat[4];      // Atitude (quaternions)
    float gyro_bias[3];          // Bias do giroscópio
    float accel_bias[3];         // Bias do acelerômetro
    float covariance[6][6];      // Matriz de covariância
    uint32_t ekf_health;         // Status do EKF
    uint32_t sensor_status;      // Status dos sensores
};
```

### 6.3 O que o sistema atual fornece

```c
// Dados disponíveis:
struct output_vector {
    uint32_t ekf_flags;          // Quais sensores completaram
    uint32_t armed_successfully; // Arming OK?
    uint32_t total_gps_drops;    // GPS dropouts
    float pos_error_ned_m[3];    // Status flags (NÃO posição)
    float att_error_rpy_deg[3];  // Status flags (NÃO atitude)
};
```

---

## 7. Soluções Alternativas

### 7.1 Habilitar Logger (Testes Futuros)

Para testes futuros, modificar `defaults.param`:

```
LOG_BACKEND_TYPE 1    # Binário
LOG_DISARMED 1       # Log mesmo desarmado
LOG_FILE_DSRMROT 1   # Rotacionar arquivo
```

Isso geraria arquivos `.bin` com todos os dados necessários para reconstrução.

### 7.2 Modificar Código para Exportar Estado

Adicionar ao `case_runner.c` ou criar hook no EKF:

```c
// Exportar estado periodicamente (ex: 10 Hz)
void export_trajectory_record(ekf3_state_t *state, FILE *out) {
    fprintf(out, "%.3f,%.6f,%.6f,%.6f,%.3f,%.3f,%.3f\n",
            get_time_ms(),
            state->position[0], state->position[1], state->position[2],
            state->velocity[0], state->velocity[1], state->velocity[2]);
}
```

### 7.3 Simulação Offline com Groundtruth

Para visualização **ilustrativa** (não reconstrução), usar os dados de groundtruth:

- Posição fixa do GPS
- Altitude do barômetro
- Dados do IMU para atitude (se necessário)
- Simular queda livre após falha

---

## 8. Conclusão Final

### Viabilidade: BAIXA

| Aspecto | Avaliação |
|---------|------------|
| **Reconstrução precisa da trajetória** | ❌ Impossível com dados atuais |
| **Animação ilustrativa simplificada** | ✅ Possível com premissas |
| **Classificação de falhas** | ✅ Possível e implementado |
| **Física da queda** | ✅ Possível e implementado |
| **Visualização do momento da falha** | ❌ Impossível sem dados temporais |
| **Detecção de causa raiz** | ❌ Impossível sem traceback |

### Recomendação

Para visualizações futuras que necessitem de trajetória:

1. **Habilitar logger interno** (`LOG_BACKEND_TYPE 1`)
2. **Modificar código** para exportar estado do EKF
3. **Gravar timestamps** de falha

Para a análise atual, a melhor abordagem é:
- Classificar falhas (feito)
- Calcular física da queda (feito)
- Criar animação ilustrativa com premissas explícitas (feito)

---

## 9. Arquivos Gerados

| Arquivo | Conteúdo | Premissa |
|---------|----------|----------|
| `drone_simulation.png` | Groundtruth + física | Hover estático |
| `failure_analysis.png` | Análise de falhas | Baseado em flags |
| `failure_timeline.png` | Timeline dos testes | Baseado em flags |
| `drone_fall_animation.gif` | Animação da queda | Queda livre teórica |
| `simulation_report.md` | Relatório completo | Todos os dados |

---

*Documento gerado em: 2026-03-07*
*Autor: OpenClaw Assistant*
*Baseado em: Análise técnica dos dados disponíveis no case EKF*
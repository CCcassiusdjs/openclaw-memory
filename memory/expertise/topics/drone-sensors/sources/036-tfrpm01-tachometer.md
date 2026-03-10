# ThunderFly TFRPM01 Tachometer

**Source:** https://docs.px4.io/main/en/sensor/thunderfly_tachometer
**Date:** 2026-03-10
**Status:** completed

## Summary

TFRPM01 é um tacômetro compacto e de baixa demanda de sistema. A placa não inclui o sensor real, mas pode ser usado com vários tipos de sensores/probes para contagem de revoluções.

## Hardware Setup

### Conexões
- **I²C**: Conecta a qualquer porta I²C do PX4
- **3-pin connector**: Conecta ao sensor/probe
- **LED**: Diagnóstico (liga quando input = ground/logical 0)

### Sensor Input
- **+5V TTL logic** ou **open collector**
- **Frequência máxima**: 20 kHz (50% duty cycle)
- **Power**: +5V do barramento I²C

### Sensor Types

#### Hall-Effect Sensor Probe
- **Vantagem**: Ideal para ambientes hostis (poeira, água)
- **Exemplo**: Littelfuse 55100 Miniature Flange Mounting Proximity Sensor
- **Funcionamento**: Magnetically operated

#### Optical Sensor Probe
- **Tipos**: Transmissive ou reflective
- **Uso**: Gerar pulsos por rotação
- **Flexibilidade**: Várias opções disponíveis

## Software Setup

### Starting Driver

```bash
# Via MAVLink Console
pcf8583 start -X -b <bus number>
```

- **-X**: External bus
- **-b**: Bus number (pode não coincidir com label do autopilot)

### Bus Number Mapping (Exemplo CUAV V5+)

| Autopilot Label | -b number |
|-----------------|-----------|
| I2C1-X | 4 |
| I2C2-X | 2 |
| I2C3-X | 1 |

### Testing

```bash
# Driver status
pcf8583 status

# Monitor RPM messages
listener rpm

# Periodic display (50 messages)
listener rpm -n 50
```

### QGroundControl MAVLink Inspector

- Analyze tools > Mavlink Inspector
- Verificar mensagem **RAW_RPM**
- Se ausente, driver não está rodando

## Parameter Setup

| Parameter | Descrição |
|-----------|-----------|
| **PCF8583_POOL** | Intervalo entre leituras |
| **PCF8583_RESET** | Valor onde contador reseta para zero |
| **PCF8583_MAGNET** | Pulsos por revolução (número de ímãs no disco) |

### Configuração Típica
- RPM lido deve corresponder a múltiplos do RPM real
- Ajustar PCF8583_MAGNET para número de pulsos/rotação

## Firmware Note

Se parâmetros não aparecem após reboot:
- Driver pode não estar no firmware
- Adicionar ao board configuration:
```bash
drivers/rpm/pcf8583
```

## Insights

1. **Logging only**: Atualmente sem uso em controle
2. **Flexible probe**: Aceita Hall-effect ou optical sensors
3. **I²C simple**: Conexão simples via I²C
4. **LED diagnostic**: Verificação manual da conexão do probe
5. **Harsh environment**: Hall-effect ideal para ambientes hostis

## Conexões

- Monitoramento de saúde de motores
- Análise de RPM pós-voo
- Potencial futuro para controle baseado em RPM
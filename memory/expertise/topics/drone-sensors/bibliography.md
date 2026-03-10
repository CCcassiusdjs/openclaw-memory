# Drone Sensors - Bibliografia

**Status:** researching
**Created:** 2026-03-10
**Priority:** 5 (Alta)

## Visão Geral

Este tópico cobre sensores utilizados em drones/UAVs: IMU, GPS, magnetômetro, barômetro, e técnicas de fusão de sensores.

## Fontes Prioritárias

### Documentação Oficial

1. **ArduPilot IMU Selection Guide** (alta prioridade)
   - URL: https://ardupilot.org/copter/docs/common-imu.html
   - Tipo: Documentação oficial
   - Status: pending

2. **PX4 Sensor Integration** (alta prioridade)
   - URL: https://docs.px4.io/main/en/sensor/
   - Tipo: Documentação oficial
   - Status: pending

3. **ArduPilot GPS for Copter** (alta prioridade)
   - URL: https://ardupilot.org/copter/docs/common-positioning-landing-page.html
   - Tipo: Documentação oficial
   - Status: pending

4. **ArduPilot Compass Configuration**
   - URL: https://ardupilot.org/copter/docs/common-compass-setup-advanced.html
   - Tipo: Documentação oficial
   - Status: pending

5. **ArduPilot Barometer**
   - URL: https://ardupilot.org/copter/docs/common-barometer.html
   - Tipo: Documentação oficial
   - Status: pending

### Tutoriais e Guias

6. **MATLAB IMU+GPS Fusion Tutorial** (já lido parcialmente)
   - URL: https://www.mathworks.com/help/nav/ug/imu-and-gps-fusion-for-inertial-navigation.html
   - Tipo: Tutorial
   - Prioridade: Alta
   - Status: pending

7. **MATLAB Inertial Sensor Fusion**
   - URL: https://www.mathworks.com/help/fusion/inertial-sensor-fusion.html
   - Tipo: Tutorial
   - Status: pending

### Papers Acadêmicos

8. **GPS-IMU Sensor Fusion for Autonomous Vehicles** (arXiv:2405.08119)
   - URL: https://arxiv.org/pdf/2405.08119
   - Tipo: Paper acadêmico
   - Status: pending

9. **GNSS/MEMS-INS Integration for Drone** (arXiv:2210.02983)
   - URL: https://arxiv.org/pdf/2210.02983
   - Tipo: Paper acadêmico
   - Status: pending

10. **ES-EKF Multi-Sensor Fusion for UAV** (arXiv:2109.04908)
    - URL: https://arxiv.org/abs/2109.04908
    - Tipo: Paper acadêmico
    - Status: completed (lido no tópico ardupilot-ekf)

### Especificações de Hardware

11. **MPU-9250/MPU-6050 Datasheet** (IMU comum)
    - URL: https://invensense.tdk.com/wp-content/uploads/2015/02/PS-MPU-9250A-01-v1.1.pdf
    - Tipo: Datasheet
    - Status: pending

12. **u-blox GPS Modules**
    - URL: https://www.u-blox.com/en/positioning-chips
    - Tipo: Documentação técnica
    - Status: pending

13. **InvenSense ICM-42688-P** (IMU high-end)
    - URL: https://invensense.tdk.com/products/motion-tracking/6-axis/
    - Tipo: Datasheet
    - Status: pending

### Livros e Referências

14. **Optimal State Estimation - Dan Simon**
    - Livro sobre Kalman Filters
    - Status: pending

15. **Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems**
    - Livro de Groves
    - Status: pending

### Blogs e Artigos

16. **PNISensor - GPS IMU Sensor Fusion**
    - URL: https://www.pnisensor.com/gps-imu-sensor-fusion-elevating-precision-in-modern-navigation-systems/
    - Tipo: Artigo técnico
    - Status: pending

17. **InertialSense - Precise Inertial Navigation**
    - URL: https://inertialsense.com/precise-inertial-navigation-through-sensor-fusion/
    - Tipo: Blog técnico
    - Status: pending

### Hardware Específico ArduPilot

18. **Pixhawk Series Sensors**
    - URL: https://ardupilot.org/copter/docs/common-pixhawk-overview.html
    - Tipo: Documentação
    - Status: pending

19. **Cube Orange Sensors**
    - URL: https://docs.cubepilot.org/
    - Tipo: Documentação
    - Status: pending

20. **DroneKit Sensors**
    - URL: https://dronekit-python.readthedocs.io/
    - Tipo: Documentação API
    - Status: pending

21. **Optical Flow Sensors**
    - URL: https://ardupilot.org/copter/docs/common-optical-flow-landing.html
    - Tipo: Documentação
    - Status: pending

## Conceitos-Chave a Estudar

- IMU (Accelerometer + Gyroscope)
- Magnetometer calibration (hard/soft iron)
- Barometer altitude estimation
- GPS accuracy and latency
- Sensor noise characteristics
- MEMS vs FOG vs other IMU types
- ADC sampling and filtering
- Low-pass filters (notch filter)
- Vibration isolation
- Temperature compensation

## Conexões com Outros Tópicos

- **ardupilot-ekf**: Fusão de sensores no EKF
- **drone-dynamics**: Como sensores medem movimento
- **flight-modes**: Sensores para modos específicos

## Notas

- Foco em sensores comuns em ArduPilot/Pixhawk
- Incluir características de ruído típicas
- Comparação entre IMUs low-cost vs high-end
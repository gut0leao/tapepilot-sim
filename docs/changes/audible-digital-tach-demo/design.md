# Design: demonstração audível do servo digital

## Arquitetura proposta

```text
Setpoint ──► seletor OFF/ON ──► atuador ──► planta ──► velocidade física
                  ▲                           │                │
                  └──── PID ◄── encoder ◄─────┘                └──► áudio
                                              ▲
                                  wow/flutter ┘
```

Em `OFF`, o PID é contornado e um comando nominal alimenta a planta. Em `ON`, o
encoder fecha a malha e o PID corrige o atuador. O áudio recebe somente a
velocidade física resultante.

## Perturbações

O primeiro modelo deve combinar componentes lentos e rápidos parametrizáveis,
com tempo e semente controlados. Valores fisicamente representativos serão
definidos depois; o primeiro objetivo é comparação reproduzível.

## Áudio

O spike pode avaliar `QMediaPlayer`, mas o MVP controlado deve preferir WAV PCM
e resampling variável. A posição na fonte avança aproximadamente por:

```text
source_position += tape_speed / nominal_tape_speed
```

Buffering e processamento devem ficar separados do tick da interface.

## Hardware

Nenhuma API deve depender de ESP32, Raspberry Pi Pico ou outra placa nesta fase.
Planta, controlador, sensor e atuador devem usar interfaces portáveis.

## Riscos

- Um modelo de planta inadequado pode produzir uma demonstração enganosa.
- Ruído aleatório não filtrado pode soar artificial.
- Resampling simples pode introduzir aliasing ou clicks.
- Um PID ajustado apenas na simulação pode não transferir para hardware real.


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

## Comando nominal e correção

O comando nominal, ou feedforward, é calibrado para que a planta nominal atinja
o setpoint em regime permanente sem perturbação ou carga adicional:

```text
OFF: comando_atuador = comando_nominal(setpoint)
ON:  comando_atuador = comando_nominal(setpoint) + correção_PID
```

Desse modo, os dois estados partem da mesma capacidade nominal e a comparação
mede o efeito da realimentação. Em `OFF`, o comando permanece fixo e não reage
ao erro. Congelar a última saída do PID foi rejeitado porque tornaria o resultado
dependente do momento da troca.

O valor numérico será derivado da escala da planta e dos limites do atuador. Ele
deve ser configurável no modelo, mas não será um controle da interface principal
no MVP.

## Unidades e limites do atuador

O atuador recebe um comando adimensional no intervalo `[-1, +1]`. A planta usa
`plant_max_rpm = 3000` como parâmetro demonstrativo configurável:

```text
comando_nominal = setpoint_rpm / plant_max_rpm
comando_solicitado = comando_nominal + correção_PID
comando_aplicado = clamp(comando_solicitado, -1, +1)
rpm_alvo = comando_aplicado * plant_max_rpm
```

Com os setpoints atuais, os comandos nominais são `0,10` em `PAUSE`, `0,60` em
`PLAY` e aproximadamente `±0,867` em `FF/REW`. O limite de 3000 RPM deixa margem
para correção e não representa ainda um motor real.

| Grandeza | Unidade interna |
|---|---|
| Tempo | segundo |
| Velocidade, setpoint e erro | RPM |
| Frequência de perturbação | hertz |
| Amplitude de perturbação | fração de `0` a `1` |
| Comando do atuador | adimensional de `-1` a `+1` |
| Ângulo visual | grau |

A interface converte a amplitude fracionária para percentual. No MVP, a razão
entre RPM física e nominal representa também a razão da velocidade linear da
fita, assumindo diâmetro constante do capstan.

## Temporização

Planta, gerador de perturbações, encoder e PID compartilham inicialmente um
passo fixo de `1 ms` (`1000 Hz`). A GUI continua solicitando atualizações em
intervalos nominais de `16 ms`, mas deixa de determinar o passo do núcleo:

```text
tempo monotônico → acumulador → passos fixos de 1 ms → estado mais recente → GUI
```

O acumulador executa os subpassos disponíveis e preserva a sobra inferior a
`1 ms`. A recuperação é limitada a `100 ms` por tick da interface. Tempo além
desse limite é descartado, gera uma indicação de atraso e não participa das
métricas comparativas.

A taxa única reduz a complexidade inicial e fornece cinquenta amostras por ciclo
para flutter de `20 Hz`. Períodos independentes para encoder e PID poderão ser
introduzidos quando houver requisitos de hardware medidos. O áudio terá sua
própria taxa de amostragem e não executará no loop de controle.

## Transição Digital Tach OFF/ON

Em `OFF → ON`, a transferência deve preservar o comando nominal no primeiro
passo. O histórico derivativo recebe a medição atual e um bias transitório
cancela a correção PID inicial:

```text
transfer_bias_inicial = -(P + I + D)
correção = P + I + D + transfer_bias
```

O `transfer_bias` decai linearmente a zero em `250 ms`, permitindo transferência
suave mesmo com `Ki = 0`. Em `ON → OFF`, o PID deixa imediatamente de consumir o
encoder. Sua última correção é reduzida linearmente até zero durante `250 ms`;
ao final, integral e histórico derivativo são limpos. As rampas são configuráveis
no modelo e não aparecem na interface principal do MVP.

A derivada atua sobre a medição, com sinal oposto, e não sobre o erro. Assim,
mudanças de setpoint não produzem pico derivativo. Testes devem distinguir o
estado estável `OFF` do curto período de saída da correção.

## Anti-windup

O termo integral é armazenado em unidades de comando e atualizado por:

```text
i_term += Ki * erro * dt
```

A integração é bloqueada quando o atuador está saturado e o sinal do erro tenta
aprofundar a saturação. Ela permanece ativa quando ajuda o comando a retornar à
faixa aplicável. Além disso:

```text
i_min = -1 - comando_nominal
i_max = +1 - comando_nominal
i_term = clamp(i_term, i_min, i_max)
```

Back-calculation foi adiado para evitar um ganho adicional `Kaw` sem necessidade
demonstrada. A telemetria expõe comando nominal, `P`, `I`, `D`, `transfer_bias`,
comandos solicitado e aplicado, saturação, tempo saturado e bloqueio da integral.

## Perturbações

O primeiro modelo combina senoides determinísticas de wow e flutter. Elas
modulam a efetividade do acionamento antes da dinâmica da planta, de modo que a
velocidade física, o encoder e o áudio observem a mesma perturbação e o PID possa
compensá-la.

| Componente | Padrão | Faixa de frequência | Faixa de amplitude |
|---|---:|---:|---:|
| Wow | `0,5 Hz`, `±1%` | `0,1–2,0 Hz` | `0–3%` |
| Flutter | `8 Hz`, `±0,3%` | `2–20 Hz` | `0–1%` |

Os presets `Wow`, `Flutter` e `Combined` são demonstrativos, não perfis medidos.
Ativação, frequência e amplitude serão configuráveis em tempo de execução. Uma
alteração preserva a fase do oscilador; ativação e desativação usam uma rampa
curta para evitar saltos. `Restaurar padrão` recupera os valores da tabela.

O gerador deve ser independente da interface e receber uma referência de tempo
controlável. Assim, a mesma configuração e o mesmo instante inicial produzem a
mesma perturbação nas execuções `OFF` e `ON`.

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

# Injeção de falhas

- **Estado:** Implemented
- **Última atualização:** 2026-08-01

## Propósito

Definir falhas físicas e de medição ajustáveis em execução.

## Escopo

- Atrito e tensão simulada.
- Wow e flutter episódicos e reproduzíveis.
- Encoder discreto, jitter, perda de pulsos e dropout.

## Fora de escopo

- Escorregamento, back-tension e modelo físico calibrado de tensão.

## Requisitos funcionais

- **FI-RF-01:** Sliders de atrito e jitter devem usar valores de 0 a 100.
- **FI-RF-02:** Esses valores devem ser convertidos para 0 a 1.
- **FI-RF-03:** A carga de atrito deve ser `tape_friction × 600`.
- **FI-RF-04:** O atrito deve reduzir o alvo por `carga × abs(comando)`.
- **FI-RF-05:** A tensão deve ser `atrito × (0.3 + 0.7 × abs(comando))`.
- **FI-RF-06:** Jitter deve atuar na medição do encoder com escala de `20 RPM`.
- **FI-RF-07:** RPM física e medida não devem ficar abaixo de zero.
- **FI-RF-08:** Wow e flutter devem ser reproduzíveis.
- **FI-RF-09:** Ocorrência, duração, taxa e intensidade devem mudar em execução.
- **FI-RF-10:** Wow e flutter devem ser independentes e somados sem estado
  `Combined`.
- **FI-RF-11:** Alterações devem preservar fase e suavizar amplitude.
- **FI-RF-12:** Restaurar padrão deve zerar ocorrências e recuperar
  `0,5 Hz/1%/3 s` e `8 Hz/0,3%/0,5 s`.
- **FI-RF-13:** Cada perfil deve usar ruído filtrado dominante, envelope,
  periodicidade residual e sementes independentes.
- **FI-RF-14:** Episódios e intervalos devem variar entre `50%` e `150%` de
  suas durações médias.
- **FI-RF-15:** O encoder deve usar `100 pulsos/revolução`, passos de `1 ms` e
  janelas de medição de `10 ms`.
- **FI-RF-16:** O jitter deve ser gaussiano e reproduzível com semente `3301`.
- **FI-RF-17:** Perda de pulsos deve variar de 0% a 100%; dropout descarta todos.
- **FI-RF-18:** A RPM bruta deve alimentar passa-baixas de primeira ordem com
  constante de `50 ms`.

## Requisitos não funcionais

- **FI-RNF-01:** Telemetria deve indicar falhas, tensão e medições do encoder.

## Critérios de aceitação

### FI-CA-01: atrito

- **Dado** o mesmo estado inicial;
- **Quando** uma execução usa atrito e outra não;
- **Então** a primeira deve produzir RPM menor e tensão positiva.

### FI-CA-02: perturbações

- **Dado** os mesmos parâmetros e sementes;
- **Quando** duas execuções avançam;
- **Então** devem produzir sinais idênticos, irregulares e independentes.

### FI-CA-03: encoder

- **Dado** `600 RPM`, 100 PPR e janela de `10 ms`;
- **Quando** não há falhas;
- **Então** devem ser observados 10 pulsos e 600 RPM bruta.

### FI-CA-04: perda e dropout

- **Dado** perda máxima ou dropout;
- **Quando** a janela avança;
- **Então** nenhum pulso deve ser observado.

## Limitações vigentes

- Parâmetros de perturbação são demonstrativos e aguardam a Issue #14.
- A tensão não possui unidade nem realimenta a planta.

## Evidências

- **Código:** `sim/faults.py`, `sim/encoder.py`, `sim/model.py`, `app.py`.
- **Testes:** testes de perturbações e encoder em `test_components.py` e
  cenários de integração headless.
- **Validação manual:** controles, episódios, filtro e dropout aprovados em 2026-08-01.


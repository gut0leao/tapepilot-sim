# Modos de transporte

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir os modos selecionáveis e seus setpoints de velocidade.

## Escopo

- Seleção de `STOP`, `PLAY`, `PAUSE`, `FF` e `REW`.
- Setpoint associado a cada modo.
- Tratamento atual de nomes desconhecidos.

## Fora de escopo

- Lei de controle da velocidade.
- Dinâmica de aceleração e frenagem.
- Aparência dos botões.

## Requisitos funcionais

- **TM-RF-01:** A interface deve oferecer `STOP`, `PLAY`, `FF`, `REW` e `PAUSE`.
- **TM-RF-02:** `STOP` deve usar setpoint de 0 RPM.
- **TM-RF-03:** `PLAY` deve usar setpoint de 1800 RPM.
- **TM-RF-04:** `PAUSE` deve usar setpoint de 300 RPM.
- **TM-RF-05:** `FF` deve usar setpoint de 2600 RPM.
- **TM-RF-06:** `REW` deve usar setpoint de 2600 RPM no comportamento vigente.
- **TM-RF-07:** Um modo desconhecido deve produzir setpoint zero e preservar o
  texto recebido no estado.

## Requisitos não funcionais

- **TM-RNF-01:** A seleção de modo deve ser testável sem abrir a interface Qt.

## Critérios de aceitação

### TM-CA-01: setpoints

- **Dado** um simulador recém-criado;
- **Quando** cada modo conhecido é selecionado e um passo é executado;
- **Então** o setpoint deve corresponder a `TM-RF-02` até `TM-RF-06`.

### TM-CA-02: seleção pela interface

- **Dado** que a janela está aberta;
- **Quando** um botão de transporte é acionado;
- **Então** o estado deve registrar o modo indicado no botão.

## Limitações vigentes

- `REW` não inverte o sentido.
- `PAUSE` representa baixa velocidade, não congelamento da simulação.
- Não há validação explícita da string recebida por `set_transport()`.

## Evidências

- **Código:** `sim/model.py`, `app.py`.
- **Testes:** `test_transport_setpoints_match_current_prototype` cobre
  `TM-RF-02` a `TM-RF-06` e `TM-RNF-01`.
- **Validação manual:** botões validados pelo proprietário em 2026-07-31.


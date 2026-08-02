# Telemetria e gráficos

- **Estado:** Implemented
- **Última atualização:** 2026-08-01

## Propósito

Definir os dados apresentados ao operador para comparar a planta, a medição e a
atuação do tacômetro digital.

## Escopo

- Telemetria textual do transporte, modelo, encoder e controlador.
- Gráficos de RPM, comando, erro, tensão e erro RMS móvel.
- Janela temporal dos dados.

## Fora de escopo

- Persistência ou exportação de telemetria.
- Cálculo das grandezas exibidas.

## Requisitos funcionais

- **TP-RF-01:** A telemetria deve permanecer acima da animação e mostrar modo,
  RPM, setpoint, comando, erro, estado do tacômetro digital, termos P/I/D,
  bias, comando solicitado e aplicado, saturação, estado do integrador, erro
  RMS, atrito, jitter, encoder bruto e filtrado, pulsos, perda, dropout,
  wow/flutter e tensão.
- **TP-RF-02:** O texto da telemetria deve ser selecionável com o mouse.
- **TP-RF-03:** A interface deve exibir gráficos de RPM, comando, erro, tensão
  e erro RMS móvel percentual.
- **TP-RF-04:** O gráfico de RPM deve distinguir setpoint, RPM física, encoder
  bruto e encoder filtrado por cor e legenda.
- **TP-RF-05:** O gráfico de comando deve distinguir valores solicitado e
  aplicado.
- **TP-RF-06:** O gráfico de erro RMS deve exibir as referências de 0,10% e
  0,20% e calcular o percentual sobre o setpoint.
- **TP-RF-07:** Os buffers devem preservar aproximadamente os últimos 20
  segundos e descartar amostras anteriores.
- **TP-RF-08:** Telemetria e gráficos devem ser atualizados após cada avanço da
  simulação.
- **TP-RF-09:** O relatório dos cenários headless deve registrar erro RMS
  físico, erro RMS máximo e tempo em saturação quando aplicáveis.

## Requisitos não funcionais

- **TP-RNF-01:** O pyqtgraph deve usar antialiasing.
- **TP-RNF-02:** O gráfico de RPM deve receber mais espaço horizontal que cada
  um dos outros gráficos.
- **TP-RNF-03:** As cores das curvas devem permanecer legíveis sobre o fundo
  escuro da interface.

## Critérios de aceitação

### TP-CA-01: atualização

- **Dado** que a aplicação está executando;
- **Quando** um tick ocorre;
- **Então** telemetria e curvas devem refletir o estado retornado pelo modelo.

### TP-CA-02: janela temporal

- **Dado** mais de 20 segundos de amostras;
- **Quando** um novo tick ocorre;
- **Então** amostras anteriores à janela devem ser removidas de todos os
  buffers.

### TP-CA-03: comparação do servo

- **Dado** o transporte em `PLAY`;
- **Quando** o tacômetro digital é alternado;
- **Então** o operador deve conseguir comparar RPM física, encoder bruto,
  encoder filtrado, atuação e erro RMS na mesma interface.

## Limitações vigentes

- Não há unidades explícitas em todos os eixos.
- Não há exportação nem pausa do histórico.
- A interface gráfica não possui testes automatizados.
- A quantização do encoder bruto pode produzir picos visuais esperados.

## Evidências

- **Código:** `app.py`, `sim/metrics.py`, `tools/run_scenarios.py`.
- **Testes:** métricas e relatórios são cobertos pelos testes unitários e pelos
  cenários headless.
- **Validação manual:** telemetria e cinco gráficos validados pelo mantenedor em
  2026-08-01.

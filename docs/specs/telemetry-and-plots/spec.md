# Telemetria e gráficos

- **Estado:** Implemented
- **Última atualização:** 2026-07-31

## Propósito

Definir os dados apresentados ao operador durante a simulação.

## Escopo

- Telemetria textual.
- Gráficos de RPM, PWM, erro e tensão.
- Janela temporal dos dados.

## Fora de escopo

- Persistência, exportação e análise estatística.
- Cálculo das grandezas exibidas.

## Requisitos funcionais

- **TP-RF-01:** A telemetria deve mostrar modo, RPM, setpoint, PWM, erro,
  atrito, jitter e tensão.
- **TP-RF-02:** O texto da telemetria deve ser selecionável com o mouse.
- **TP-RF-03:** A interface deve exibir gráficos de RPM desejada e simulada,
  PWM, erro e tensão.
- **TP-RF-04:** Os buffers devem preservar aproximadamente os últimos 20
  segundos e descartar amostras anteriores.
- **TP-RF-05:** Os gráficos devem ser atualizados após cada passo da simulação.

## Requisitos não funcionais

- **TP-RNF-01:** O pyqtgraph deve usar antialiasing.
- **TP-RNF-02:** O gráfico de RPM deve receber mais espaço horizontal que cada
  um dos outros gráficos.

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

## Limitações vigentes

- As curvas de RPM não possuem legenda.
- Não há unidades explícitas nos eixos.
- Não há exportação nem pausa do histórico.
- A interface não possui testes automatizados.

## Evidências

- **Código:** `app.py`.
- **Testes:** não há cobertura automatizada da interface.
- **Validação manual:** telemetria e gráficos validados em 2026-07-31.


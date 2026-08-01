# Transporte reverso

- **Estado:** Draft
- **Data:** 2026-07-31
- **Specs afetadas:** `transport-modes`, `speed-control`,
  `mechanics-visualization`, `telemetry-and-plots`
- **Issue:** [#9 — Implementar transporte reverso com RPM negativa](https://github.com/gut0leao/tapepilot-sim/issues/9)

## Problema

`FF` e `REW` usam atualmente o mesmo setpoint positivo de 2600 RPM. O sistema
não distingue avanço rápido de retrocesso na dinâmica, telemetria ou animação.

## Objetivo

Representar `REW` por velocidade negativa em todo o fluxo observável.

## Fora de escopo

- Motores independentes para as bobinas.
- Modelo realista de frenagem e tensão.
- Alterações em `PLAY` e `FF` sem relação com a transição reversa.

## Impacto

- Setpoint e transições dos modos.
- Planta e cálculo do atrito.
- Telemetria e gráfico de RPM.
- Sentido da animação.
- Testes de caracterização atuais.

## Questões em aberto

- A transição direta deve frear antes de inverter ou atravessar zero
  continuamente no modelo de primeira ordem?
- As duas bobinas devem compartilhar o mesmo sinal visual do capstan?

## Evidências de implementação

- **Preparação:** núcleo independente de Qt e testes de caracterização já
  existentes.
- **Código funcional:** ainda não implementado.
- **Testes do delta:** ainda não implementados.
- **Validação manual:** pendente.
- **Commit/PR:** pendente.
- **Limitações remanescentes:** a definir após aprovação.

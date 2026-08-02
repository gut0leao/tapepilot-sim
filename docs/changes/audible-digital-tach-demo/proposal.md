# Demonstração audível do servo digital

- **Estado:** Draft
- **Data:** 2026-08-01
- **Specs afetadas:** `telemetry-and-plots`, `simulation-runtime`; nova
  capacidade `audio-playback`
- **Issue:** [#10 — Demonstrar estabilização audível do servo digital](https://github.com/gut0leao/tapepilot-sim/issues/10)
- **Dependência:** [Fundamentos do servo digital](../archive/2026-08-01-digital-servo-foundations/proposal.md)

## Problema

Métricas e gráficos não tornam imediatamente perceptível o efeito das variações
de velocidade. A demonstração precisa transformar a velocidade física produzida
pelo núcleo em variação audível e permitir comparar `Digital Tach OFF/ON`.

## Objetivo

Reproduzir uma amostra WAV conforme a velocidade física simulada e apresentar
uma comparação auditiva e quantitativa entre malha aberta e fechada.

## Fora de escopo

- Implementar planta, encoder, perturbações ou PID, cobertos pela change de
  fundamentos.
- Simular eletrônica de áudio, ruído ou resposta em frequência da fita.
- Suportar MP3 no MVP.
- Escolher hardware embarcado ou alegar desempenho em tape decks reais.

## Impacto

- Carregamento de assets WAV independente do diretório de execução.
- Reprodução em velocidade variável.
- Controle de comparação `Digital Tach OFF/ON`.
- Métricas e gráficos orientados à demonstração.
- Nova capacidade AS-IS `audio-playback` depois da implementação.

## Questões em aberto

- Qual estratégia de resampling atenderá ao MVP sem clicks perceptíveis?
- O áudio deve silenciar ou desacelerar durante a partida abaixo de uma RPM
  mínima?
- A comparação será somente ao vivo ou também terá reprodução A/B registrada?

## Evidências de implementação

- **Código:** ainda não implementado.
- **Testes:** ainda não implementados.
- **Validação manual:** pendente.
- **Commit/PR:** pendente.
- **Limitações remanescentes:** a definir após o spike de áudio.

# Demonstração audível do servo digital

- **Estado:** Draft
- **Data:** 2026-08-01
- **Specs afetadas:** `transport-modes`, `speed-control`, `fault-injection`,
  `telemetry-and-plots`, `simulation-runtime`; nova capacidade
  `audio-playback`
- **Issue:** [#10 — Demonstrar estabilização audível do servo digital](https://github.com/gut0leao/tapepilot-sim/issues/10)

## Problema

O modelo atual possui um controlador proporcional sempre ativo, uma planta
simplificada e jitter apenas visual. Ele não permite comparar uma operação
degradada sem controle digital com um servo PID, nem ouvir o efeito da correção
na velocidade física da fita.

## Objetivo

Permitir uma comparação reproduzível entre `Digital Tach OFF` e `Digital Tach
ON`, tornando wow e flutter audíveis em uma amostra e mensuráveis nos gráficos.

## Fora de escopo

- Simular ruído, saturação, resposta em frequência ou qualidade da fita.
- Suportar MP3 no primeiro MVP; WAV PCM é suficiente.
- Escolher uma plataforma embarcada.
- Afirmar desempenho em tape decks reais sem medições.

## Impacto

- Separação entre planta, controlador e encoder.
- Controlador PID ativável.
- Perturbações físicas reproduzíveis.
- Reprodução de áudio em velocidade variável.
- Novas métricas e controles de comparação.
- Nova capacidade AS-IS de áudio após a implementação.

## Questões em aberto

- Quais amplitudes e frequências representarão os perfis iniciais de wow e
  flutter?
- Qual comando nominal será usado com `Digital Tach OFF`?
- Qual estratégia de resampling atenderá ao MVP sem clicks perceptíveis?
- O áudio deve silenciar ou desacelerar durante a partida abaixo de uma RPM
  mínima?
- A comparação será feita somente por alternância ao vivo ou também por
  reprodução A/B de execuções registradas?

## Evidências de implementação

- **Código:** ainda não implementado.
- **Testes:** ainda não implementados.
- **Validação manual:** pendente.
- **Commit/PR:** pendente.
- **Limitações remanescentes:** a definir após o spike de áudio.


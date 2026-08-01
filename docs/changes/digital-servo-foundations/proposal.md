# Fundamentos do servo digital

- **Estado:** In Progress
- **Data:** 2026-08-01
- **Specs afetadas:** `speed-control`, `fault-injection`,
  `telemetry-and-plots`, `simulation-runtime`
- **Issues:** [#4](https://github.com/gut0leao/tapepilot-sim/issues/4),
  [#12](https://github.com/gut0leao/tapepilot-sim/issues/12),
  [#5](https://github.com/gut0leao/tapepilot-sim/issues/5) e
  [#7](https://github.com/gut0leao/tapepilot-sim/issues/7)

## Problema

O protótipo concentra planta, controlador, falhas e movimento em um único passo
ligado à GUI. O PWM não é uma entrada efetiva da planta, o jitter é apenas
visual e não existem encoder, PID ou perturbações físicas reproduzíveis.

## Objetivo

Estabelecer um núcleo determinístico e portátil para comparar comando nominal em
malha aberta com servo PID em malha fechada, antes da reprodução de áudio.

## Fora de escopo

- Reprodução ou processamento de áudio.
- Controles finais da demonstração na interface.
- Escolha de hardware embarcado.
- Parâmetros identificados em um mecanismo real.
- Alteração do sentido vigente de `REW`.

## Impacto

- Separação entre estado, planta, controlador, encoder, perturbações e métricas.
- Atuador normalizado e planta comandada explicitamente.
- Núcleo em passo fixo independente da GUI.
- Wow e flutter determinísticos e configuráveis.
- Perturbações naturais, filtradas e reproduzíveis, sem senoide dominante.
- PID com transferência suave, saturação e anti-windup.
- Telemetria interna suficiente para validar o controle.

## Questões em aberto

Nenhuma decisão bloqueadora. Os valores do modelo são demonstrativos e deverão
ser revistos depois de medições em hardware real.

## Decisões de perturbação

Wow e flutter usam ruído colorido como componente dominante, envelope variável
e apenas `15%` e `10%` de periodicidade residual. Possuem controles independentes
de taxa característica e intensidade `Dry/Wet`, com sementes fixas distintas.

## Evidências de implementação

- **Código:** componentes extraídos em `sim/state.py`, `controller.py`,
  `plant.py`, `faults.py` e `encoder.py`; scheduler fixo e wow/flutter estão
  implementados localmente para revisão; encoder discreto e PID ainda pendem.
- **Testes:** vinte testes passam, incluindo scheduler, independência,
  irregularidade e reprodutibilidade das perturbações;
  workflow [Quality 30703602470](https://github.com/gut0leao/tapepilot-sim/actions/runs/30703602470) aprovado.
- **Validação manual:** interface e controles naturais de wow/flutter aprovados
  pelo mantenedor em 2026-08-01, sem regressões aparentes.
- **Commit/PR:** commit `6e58f98` implementa a extração da Issue #4.
- **Limitações remanescentes:** parâmetros ainda não identificados fisicamente.

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

## Decisões tomadas

- O MVP terá perfis determinísticos `Wow`, `Flutter` e `Combined`.
- Wow começará com `0,5 Hz` e amplitude de `±1%`; flutter, com `8 Hz` e
  `±0,3%`. São valores demonstrativos, não medições de um equipamento real.
- Frequência, amplitude e ativação de cada componente poderão ser alteradas em
  tempo de execução, com ação imediata e fase contínua.
- As faixas iniciais serão `0,1–2,0 Hz` e `0–3%` para wow, e `2–20 Hz` e
  `0–1%` para flutter.
- A perturbação atuará na efetividade do acionamento da planta. Alterações e
  desligamentos usarão transição suave para não introduzir saltos artificiais.
- Os padrões poderão ser restaurados e a mesma configuração será usada nas
  comparações `Digital Tach OFF` e `ON`.
- O comando nominal será calibrado para atingir o setpoint em regime permanente
  com a planta nominal, sem perturbação ou carga adicional. Em `OFF`, ele fica
  fixo; em `ON`, o PID acrescenta sua correção à mesma base.
- O comando nominal será configurável no modelo, mas não ficará exposto na
  interface principal do MVP. Seu valor numérico depende da definição da escala
  do atuador.
- O atuador usará comando normalizado entre `-1` e `+1`, e a planta terá
  `plant_max_rpm = 3000` como valor demonstrativo configurável. O comando
  nominal será `setpoint_rpm / plant_max_rpm`.
- O comando total, formado pelo nominal mais a correção PID, será saturado nos
  limites do atuador. RPM continuará sendo a unidade de velocidade do MVP;
  amplitudes serão frações internamente e percentuais na interface.
- Planta, perturbações, encoder e PID serão executados inicialmente a `1000 Hz`,
  com passo fixo de `1 ms`; a GUI permanecerá próxima de `60 Hz` e apenas
  apresentará o estado mais recente.
- O runtime acumulará tempo monotônico e executará subpassos, limitando a
  recuperação a `100 ms`. Excedentes serão descartados e sinalizados, sem entrar
  nas métricas da demonstração.
- A troca `OFF → ON` usará transferência sem salto: histórico derivativo
  inicializado pela medição atual e `transfer_bias` preparado para correção
  inicial zero, inclusive com `Ki = 0`. O bias decairá em `250 ms`. Em
  `ON → OFF`, o PID para de atualizar e sua última correção também decai
  linearmente até zero em `250 ms`; depois seus estados são limpos.
- A derivada será calculada sobre a medição para evitar picos quando o setpoint
  mudar. A rampa de desligamento será configurável no modelo, não na interface
  principal do MVP.
- O anti-windup usará integração condicional: a integral será bloqueada quando o
  erro aprofundar a saturação e liberada quando ajudar a sair dela. O termo
  integral também respeitará a margem entre o comando nominal e `[-1, +1]`;
  back-calculation e o parâmetro `Kaw` ficam fora do MVP.
- A telemetria distinguirá comando nominal, termos `P/I/D`, `transfer_bias`,
  comandos solicitado e aplicado, saturação, tempo saturado e bloqueio da
  integral.

## Questões em aberto

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

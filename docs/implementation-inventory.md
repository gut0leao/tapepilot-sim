# Inventário da implementação

Este documento relaciona o que está versionado à sua documentação e validação.
Ele cobre responsabilidades e comportamentos relevantes, não detalhes internos
sem efeito observável.

## Artefatos

| Artefato | Responsabilidade | Contrato vigente | Validação |
|---|---|---|---|
| `app.py` | Inicialização, janela Qt, controles, telemetria, cena e gráficos | `simulation-runtime`, `transport-modes`, `mechanics-visualization`, `telemetry-and-plots` | compilação; validação visual manual |
| `sim/model.py` | Fachada e coordenação do passo, transporte e ângulos | `speed-control`, `fault-injection`, `transport-modes`, `mechanics-visualization` | `tests/test_simulator.py` |
| `sim/state.py` | Estado instantâneo compartilhado | `simulation-runtime` | importação e testes do simulador |
| `sim/controller.py` | Comando nominal, PID, transições e anti-windup | `speed-control` | `tests/test_components.py` |
| `sim/plant.py` | Resposta de primeira ordem vigente | `speed-control` | `tests/test_components.py` |
| `sim/faults.py` | Carga de atrito e indicador de tensão vigentes | `fault-injection` | `tests/test_components.py` |
| `sim/encoder.py` | Encoder discreto, jitter, perda de pulsos e dropout | `fault-injection` | `tests/test_components.py` |
| `sim/runtime.py` | Conversão de tempo real em passos fixos limitados | `simulation-runtime` | `tests/test_components.py` |
| `sim/metrics.py` | Erro RMS percentual após estabilização | `speed-control`, `telemetry-and-plots` | `tests/test_metrics.py` |
| `sim/__init__.py` | API pública de `SimState` e `Simulator` | `simulation-runtime` | importação pelos testes |
| `assets/svg/*.svg` | Bobinas e capstan da cena | `mechanics-visualization` | carregamento visual manual |
| `tests/test_simulator.py` | Caracterização do modelo atual | `development.md` | `unittest` e `pytest` |
| `tests/test_components.py` | Contratos dos componentes extraídos | specs de controle, falhas e runtime | `unittest` e `pytest` |
| `tools/check_docs.py` | Links e estrutura documental | `simulation-runtime`, `development.md` | execução local e CI |
| `tools/run_scenarios.py` | Integração headless por cenários, CSV, resumo e expectativas | Issue #15 | `tests/test_scenarios.py` e CI |
| `tests/scenarios/*.json` | Entradas e oráculos dos testes de integração | Issues #7 e #15 | runner headless |
| `.github/workflows/quality.yml` | Validação contínua | `simulation-runtime` | GitHub Actions |
| `pyproject.toml` | Metadados, dependências e configuração de testes | `simulation-runtime`, `development.md` | instalação do pacote |
| `LICENSE` | Termos de distribuição MIT | `README.md` | revisão textual |

## Comportamentos da interface

| Comportamento implementado | Spec vigente |
|---|---|
| Janela inicial de 1200 × 700 px | `simulation-runtime` (`SR-RF-01`) |
| Cena com duas bobinas e um capstan | `mechanics-visualization` (`MV-RF-01`) |
| Escala de 180 px para bobinas e 70 px para capstan | `mechanics-visualization` (`MV-RF-02`, `MV-RF-03`) |
| Pivô no centro do SVG | `mechanics-visualization` (`MV-RF-05`) |
| Botões `STOP`, `PLAY`, `FF`, `REW` e `PAUSE` | `transport-modes` (`TM-RF-01`) |
| Sliders de atrito e jitter na faixa 0–100 | `fault-injection` (`FI-RF-01`) |
| Telemetria selecionável | `telemetry-and-plots` (`TP-RF-02`) |
| Cinco gráficos com janela de 20 segundos | `telemetry-and-plots` (`TP-RF-03` a `TP-RF-08`) | validação visual manual |
| Atualização nominal de 16 ms usando relógio monotônico | `simulation-runtime` (`SR-RF-02`, `SR-RF-03`) |

## Comportamentos do modelo

| Comportamento implementado | Requisito | Teste atual |
|---|---|---|
| Setpoints por modo | `TM-RF-02` a `TM-RF-06` | `test_transport_setpoints_match_current_prototype` |
| Modo desconhecido com setpoint zero | `TM-RF-07` | ainda não coberto |
| Comando nominal e PID ajustável | `speed-control` (`SC-RF-08` a `SC-RF-17`) | testes de PID em `test_components.py` e `test_simulator.py` |
| Resposta de primeira ordem | `SC-RF-04` | `test_first_order_response_uses_elapsed_time` |
| Carga equivalente de atrito | `FI-RF-03`, `FI-RF-04` | `test_friction_reduces_speed_and_produces_tension` |
| Indicador de tensão sem unidade | `FI-RF-05` | teste de atrito |
| Encoder discreto, filtro e falhas | `fault-injection` (`FI-RF-15` a `FI-RF-18`) | testes de encoder em `test_components.py` |
| Wow e flutter naturais, parametrizáveis e reproduzíveis | `fault-injection` (`FI-RF-08` a `FI-RF-14`) | testes de perturbação em `test_components.py` |
| Scheduler de 1 ms com recuperação limitada | `simulation-runtime` (`SR-RF-06`, `SR-RF-07`) | testes do scheduler em `test_components.py` |
| Movimento angular proporcional | `MV-RF-06` | `test_angles_advance_in_current_positive_direction` |
| Normalização angular em 360 graus | `MV-RF-07` | ainda não coberto |
| Convergência de `STOP` para zero | `SC-RF-05` | `test_stop_converges_toward_zero` |

## Lacunas de validação conhecidas

Todo comportamento relevante está descrito, mas nem todo comportamento está
automatizado. Permanecem dependentes de teste manual ou sem teste dedicado:

- construção e interação da janela Qt;
- carregamento, posição e rotação visual dos SVGs;
- atualização e descarte dos buffers dos gráficos;
- fallback de modos desconhecidos;
- normalização angular após múltiplas voltas.

Essas lacunas são de validação, não de documentação, e devem orientar a futura
ampliação da suíte de testes.

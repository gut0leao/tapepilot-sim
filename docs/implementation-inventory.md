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
| `sim/controller.py` | Controle proporcional e saturação vigentes | `speed-control` | `tests/test_components.py` |
| `sim/plant.py` | Resposta de primeira ordem vigente | `speed-control` | `tests/test_components.py` |
| `sim/faults.py` | Carga de atrito e indicador de tensão vigentes | `fault-injection` | `tests/test_components.py` |
| `sim/encoder.py` | Jitter aplicado à medição visual vigente | `fault-injection` | `tests/test_components.py` |
| `sim/__init__.py` | API pública de `SimState` e `Simulator` | `simulation-runtime` | importação pelos testes |
| `assets/svg/*.svg` | Bobinas e capstan da cena | `mechanics-visualization` | carregamento visual manual |
| `tests/test_simulator.py` | Caracterização do modelo atual | `development.md` | `unittest` e `pytest` |
| `tests/test_components.py` | Contratos dos componentes extraídos | change `digital-servo-foundations` | `unittest` e `pytest` |
| `tools/check_docs.py` | Links e estrutura documental | `simulation-runtime`, `development.md` | execução local e CI |
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
| Quatro gráficos com janela de 20 segundos | `telemetry-and-plots` (`TP-RF-03`, `TP-RF-04`) |
| Atualização nominal de 16 ms usando relógio monotônico | `simulation-runtime` (`SR-RF-02`, `SR-RF-03`) |

## Comportamentos do modelo

| Comportamento implementado | Requisito | Teste atual |
|---|---|---|
| Setpoints por modo | `TM-RF-02` a `TM-RF-06` | `test_transport_setpoints_match_current_prototype` |
| Modo desconhecido com setpoint zero | `TM-RF-07` | ainda não coberto |
| Controle proporcional com saturação | `SC-RF-01` a `SC-RF-03` | `test_pwm_is_saturated` |
| Resposta de primeira ordem | `SC-RF-04` | `test_first_order_response_uses_elapsed_time` |
| Carga equivalente de atrito | `FI-RF-03`, `FI-RF-04` | `test_friction_reduces_speed_and_produces_tension` |
| Indicador de tensão sem unidade | `FI-RF-05` | teste de atrito |
| Jitter gaussiano somente visual | `FI-RF-06`, `FI-RF-07` | `test_encoder_preserves_visual_jitter` |
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

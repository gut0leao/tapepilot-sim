# Inventário da implementação

Este documento relaciona o que está versionado à sua documentação e validação.
Ele cobre responsabilidades e comportamentos relevantes, não detalhes internos
sem efeito observável.

## Artefatos

| Artefato | Responsabilidade | Documentação principal | Validação |
|---|---|---|---|
| `app.py` | Inicialização, janela Qt, controles, telemetria, cena e gráficos | `architecture.md`, `user-guide.md` | compilação; validação visual manual |
| `sim/model.py` | Estado, controle proporcional, dinâmica, falhas e ângulos | `simulation-model.md` | `tests/test_simulator.py` |
| `sim/__init__.py` | API pública de `SimState` e `Simulator` | `architecture.md` | importação pelos testes |
| `assets/svg/*.svg` | Bobinas e capstan da cena | `architecture.md`, `user-guide.md` | carregamento visual manual |
| `tests/test_simulator.py` | Caracterização do modelo atual | `development.md` | `unittest` e `pytest` |
| `tools/check_docs.py` | Links locais e estrutura mínima das specs | `development.md` | execução local e CI |
| `.github/workflows/quality.yml` | Validação contínua | `development.md` | GitHub Actions |
| `pyproject.toml` | Metadados, dependências e configuração de testes | `README.md`, `development.md` | instalação do pacote |
| `LICENSE` | Termos de distribuição MIT | `README.md` | revisão textual |

## Comportamentos da interface

| Comportamento implementado | Documento |
|---|---|
| Janela inicial de 1200 × 700 px | `user-guide.md` |
| Cena com duas bobinas e um capstan | `user-guide.md` |
| Escala de 180 px para bobinas e 70 px para capstan | `architecture.md`, `user-guide.md` |
| Pivô no centro do SVG | `user-guide.md` |
| Botões `STOP`, `PLAY`, `FF`, `REW` e `PAUSE` | `user-guide.md`, `simulation-model.md` |
| Sliders de atrito e jitter na faixa 0–100 | `user-guide.md` |
| Telemetria selecionável | `user-guide.md` |
| Quatro gráficos com janela de 20 segundos | `architecture.md`, `user-guide.md` |
| Atualização nominal de 16 ms usando relógio monotônico | `architecture.md`, `simulation-model.md` |

## Comportamentos do modelo

| Comportamento implementado | Documento | Teste atual |
|---|---|---|
| Setpoints por modo | `simulation-model.md` | `test_transport_setpoints_match_current_prototype` |
| Modo desconhecido com setpoint zero | `simulation-model.md` | ainda não coberto |
| Controle proporcional com saturação | `simulation-model.md` | `test_pwm_is_saturated` |
| Resposta de primeira ordem | `simulation-model.md` | `test_first_order_response_uses_elapsed_time` |
| Carga equivalente de atrito | `simulation-model.md` | `test_friction_reduces_speed_and_produces_tension` |
| Indicador de tensão sem unidade | `simulation-model.md` | teste de atrito |
| Jitter gaussiano somente visual | `simulation-model.md` | ainda não coberto |
| Movimento angular proporcional | `simulation-model.md` | `test_angles_advance_in_current_positive_direction` |
| Normalização angular em 360 graus | `simulation-model.md` | ainda não coberto |
| Convergência de `STOP` para zero | `simulation-model.md` | `test_stop_converges_toward_zero` |

## Lacunas de validação conhecidas

Todo comportamento relevante está descrito, mas nem todo comportamento está
automatizado. Permanecem dependentes de teste manual ou sem teste dedicado:

- construção e interação da janela Qt;
- carregamento, posição e rotação visual dos SVGs;
- atualização e descarte dos buffers dos gráficos;
- efeito estatístico do jitter;
- fallback de modos desconhecidos;
- normalização angular após múltiplas voltas.

Essas lacunas são de validação, não de documentação, e devem orientar a futura
ampliação da suíte de testes.


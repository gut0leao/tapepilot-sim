# Specs de capacidade

## Objetivo

As specs deste diretório descrevem o comportamento vigente do TapePilot. Cada
uma representa uma capacidade coesa do sistema e funciona como fonte de verdade
para seus requisitos observáveis.

As specs são documentos vivos: depois que uma mudança é implementada e
validada, o delta aprovado é incorporado à spec afetada. O histórico permanece
no Git e na proposta arquivada em `docs/changes/archive/`.

## Capacidades

| Capacidade | Estado | Responsabilidade |
|---|---|---|
| [Modos de transporte](transport-modes/spec.md) | `Implemented` | modos, setpoints e seleção |
| [Controle de velocidade](speed-control/spec.md) | `Implemented` | erro, controlador e resposta |
| [Injeção de falhas](fault-injection/spec.md) | `Implemented` | atrito, jitter e tensão |
| [Visualização mecânica](mechanics-visualization/spec.md) | `Implemented` | SVGs, escalas e movimento |
| [Telemetria e gráficos](telemetry-and-plots/spec.md) | `Implemented` | dados exibidos e histórico |
| [Runtime da simulação](simulation-runtime/spec.md) | `Implemented` | temporização, separação e execução |

## Granularidade

Uma spec agrupa requisitos que:

- pertencem ao mesmo conceito do domínio;
- costumam mudar pelo mesmo motivo;
- podem ser validados como uma capacidade coerente;
- possuem responsabilidades técnicas próximas.

Não se cria uma spec por botão ou fórmula, nem uma única spec para toda a
aplicação. Uma nova capacidade nasce por meio de uma change e, quando passa a
existir, ganha uma spec baseada em [`template.md`](template.md).

## Estados

| Estado | Significado |
|---|---|
| `Draft` | documentação inicial de uma capacidade vigente sendo preparada |
| `Implemented` | comportamento vigente e evidências registradas |
| `Superseded` | capacidade substituída por outra organização |

`Approved` e `In Progress` pertencem às changes, não às specs AS-IS.

## Alterando uma capacidade

Mudanças observáveis não são editadas diretamente na spec vigente antes da
implementação. Elas começam em `docs/changes/<nome>/`:

```text
proposal.md
spec-delta.md
design.md
tasks.md
```

O fluxo completo está em [Processo de mudanças](../changes/README.md).

Os `tasks.md` das capacidades registram o estabelecimento do baseline. Tarefas
de mudanças posteriores permanecem nas changes arquivadas e não são copiadas
para esses arquivos.

## Definition of Done

Uma mudança está pronta quando:

- o delta aprovado foi implementado;
- critérios de aceitação possuem evidência;
- testes relevantes passam;
- specs afetadas representam o novo comportamento;
- documentação clássica foi atualizada;
- limitações remanescentes foram registradas;
- a proposta foi movida para `docs/changes/archive/`.

## Rastreabilidade

Cada capacidade usa um prefixo estável nos requisitos:

| Prefixo | Capacidade |
|---|---|
| `TM` | modos de transporte |
| `SC` | controle de velocidade |
| `FI` | injeção de falhas |
| `MV` | visualização mecânica |
| `TP` | telemetria e gráficos |
| `SR` | runtime da simulação |

Testes e deltas devem citar esses identificadores quando aplicável.

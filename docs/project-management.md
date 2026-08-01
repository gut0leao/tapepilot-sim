# Gestão do projeto

Este documento define como o trabalho do TapePilot é organizado. O repositório
mantém regras, requisitos e decisões; GitHub Issues e GitHub Projects mantêm o
estado operacional do trabalho.

```text
Roadmap → Product Backlog → Ready → In Progress → Review → Done
```

A sprint seleciona um conjunto de itens em `Ready`; ela não é um estado do
fluxo.

## 1. Roadmap

O [roadmap](roadmap.md) registra direções futuras sem compromisso imediato de
implementação. Quando uma ideia se torna candidata real a desenvolvimento, ela
é criada como Issue no product backlog.

## 2. Product backlog

O backlog é mantido em GitHub Issues. Cada Issue deve:

- descrever um resultado, não apenas uma atividade;
- possuir prioridade;
- referenciar a change correspondente, quando houver;
- evitar copiar requisitos já mantidos nas specs ou no delta.

Ideias ainda vagas podem permanecer no roadmap sem Issue.

## 3. GitHub Project

O GitHub Project organiza as Issues usando os estados:

```text
Backlog → Ready → In Progress → Review → Done
```

Configuração-alvo:

- `Status`: estado do fluxo;
- `Priority`: ordem relativa de execução;
- `Sprint`: ciclo em que o item será trabalhado.

O Project mostra o estado atual. Ele não substitui requisitos, design ou
decisões versionadas no repositório.

### Configuração vigente

O [Project `tapepilot-sim`](https://github.com/users/gut0leao/projects/2), número
2, foi configurado em 2026-07-31 com os cinco estados e os campos `Priority` e
`Sprint` descritos acima. `Sprint 1` foi concluída com a publicação da base
spec-driven. Não há sprint ativa; novos itens permanecem `Unscheduled` até
satisfazerem a Definition of Ready.

## 4. Changes e Definition of Ready

Mudanças observáveis são detalhadas em [docs/changes](changes/README.md). Um item
pode passar para `Ready` quando:

- problema e resultado esperado estão claros;
- specs afetadas foram identificadas;
- o delta possui critérios verificáveis;
- decisões bloqueadoras foram resolvidas;
- a change está em `Approved`;
- o trabalho cabe em uma sprint ou foi dividido.

Correções que apenas restauram um requisito vigente podem dispensar uma change.

## 5. Sprint

Cada sprint deve possuir:

- um objetivo curto e observável;
- um conjunto pequeno de Issues em `Ready`;
- duração ou escopo definido;
- review ao final.

A Issue representa o item no backlog. O `tasks.md` da change contém a
decomposição técnica. A mesma checklist não deve ser copiada para os dois locais.

Durante a execução, o item percorre `In Progress` e `Review`. Trabalho não
concluído volta ao backlog ou à sprint seguinte de forma explícita.

## 6. Conclusão

Uma Issue pode ir para `Done` quando a
[Definition of Done](specs/README.md#definition-of-done) foi satisfeita:

- implementação e testes estão concluídos;
- critérios de aceitação possuem evidência;
- delta foi incorporado às specs vigentes;
- documentação clássica e changelog foram atualizados;
- change foi arquivada;
- workflow de qualidade passou.

A review registra na Issue ou pull request o resultado, o que ficou de fora e
eventuais ações de retrospectiva. Só se cria documentação adicional quando a
informação tiver valor duradouro.

## Responsabilidade de cada artefato

| Artefato | Responsabilidade |
|---|---|
| `docs/roadmap.md` | direção futura |
| GitHub Issues | product backlog e unidade de entrega |
| GitHub Project | prioridade, sprint e estado atual |
| `docs/changes/` | mudança proposta e delta de requisitos |
| `docs/specs/` | comportamento vigente |
| `docs/decisions/` | decisões técnicas duradouras |
| `CHANGELOG.md` | mudanças relevantes já entregues |

# Processo de especificações

## Objetivo

Uma spec define o comportamento esperado antes da implementação. Dentro de seu
escopo, ela é a fonte de verdade para requisitos e critérios de aceitação.

Documentos em `architecture.md` e `simulation-model.md` explicam como o sistema
é hoje. As specs descrevem uma mudança desejada até que ela seja implementada e
incorporada à documentação corrente.

## Quando uma spec é necessária

Crie ou atualize uma spec quando a mudança:

- adiciona uma funcionalidade;
- altera comportamento observável;
- modifica equações ou premissas do modelo;
- introduz um componente ou interface relevante;
- necessita de vários critérios de aceitação.

Uma spec própria normalmente não é necessária para:

- correção de texto ou formatação;
- renomeação interna sem efeito de comportamento;
- atualização de dependência sem mudança funcional;
- correção pequena que restaura um requisito já documentado.

Se houver dúvida, prefira uma spec curta.

## Estrutura de uma funcionalidade

```text
docs/specs/<nome-da-funcionalidade>/
├── spec.md
├── design.md
└── tasks.md
```

- `spec.md`: problema, escopo, requisitos e critérios de aceitação;
- `design.md`: solução técnica, alternativas e riscos;
- `tasks.md`: trabalho executável e verificável.

Copie [`template.md`](template.md) para iniciar uma proposta.

## Estados

| Estado | Significado |
|---|---|
| `Draft` | Em elaboração; ainda pode mudar livremente |
| `Approved` | Escopo aceito e pronto para implementação |
| `In Progress` | Implementação em andamento |
| `Implemented` | Critérios satisfeitos e documentação atualizada |
| `Superseded` | Substituída por outra spec |

Somente uma decisão consciente deve mover a spec para `Approved`. Marcar como
`Implemented` exige evidência de validação, preferencialmente testes.

## Fluxo

1. Descrever problema, objetivo e limites em `spec.md`.
2. Tornar cada requisito observável e numerado.
3. Revisar questões em aberto e aprovar a spec.
4. Registrar a solução em `design.md`.
5. Dividir o trabalho em `tasks.md`.
6. Implementar e validar os critérios de aceitação.
7. Atualizar a documentação clássica.
8. Marcar a spec como `Implemented`.

## Definition of Done

Uma funcionalidade está pronta quando:

- todos os requisitos aprovados foram implementados;
- todos os critérios de aceitação possuem evidência de validação;
- os testes relevantes passam;
- a documentação clássica descreve o comportamento resultante;
- limitações conhecidas foram registradas;
- `tasks.md` reflete o trabalho concluído;
- a spec está marcada como `Implemented`.

## Linguagem normativa

- **Deve:** requisito obrigatório.
- **Não deve:** proibição obrigatória.
- **Pode:** comportamento permitido ou opcional.

Evite descrever detalhes de implementação em requisitos. “A RPM deve convergir
para um valor negativo” é requisito; “usar uma variável chamada `direction`” é
design.

## Rastreabilidade

Requisitos usam identificadores como `RF-01` e `RNF-01`. Testes relacionados
devem mencionar esses identificadores no nome, comentário ou docstring quando
isso ajudar a localizar a evidência.

`tasks.md` não substitui a spec: concluir todas as tarefas não significa que os
critérios de aceitação foram necessariamente satisfeitos.

## Evidências

Ao concluir a implementação, registre na spec:

- arquivos de implementação;
- testes e requisitos cobertos;
- validações manuais necessárias;
- commit ou pull request, quando houver;
- limitações remanescentes.

## Índice

| Spec | Estado | Requisitos | Implementação |
|---|---|---:|---|
| [Transporte reverso](reverse-transport/spec.md) | `Draft` | RF-01–RF-07 | — |

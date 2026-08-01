# ADR 0001: Processo híbrido de documentação

- **Estado:** Aceito
- **Data:** 2026-07-31

> A organização das specs definida aqui foi refinada pelo
> [ADR 0002](0002-specs-vivas-e-deltas-de-mudanca.md).

## Contexto

O TapePilot começou como um protótipo em um único arquivo. O README original
misturava funcionalidades existentes com uma arquitetura ainda planejada.

O projeto precisa de maior controle sobre requisitos e implementação, mas ainda
é pequeno demais para justificar um processo formal pesado em toda mudança.

## Decisão

Será adotado um processo híbrido:

- documentação clássica descreve arquitetura, desenvolvimento e modelo atual;
- ADRs registram decisões técnicas duradouras;
- specs definem novas funcionalidades e mudanças observáveis antes da
  implementação;
- correções pequenas que restauram comportamento já definido podem ser feitas
  sem uma spec exclusiva.

Uma funcionalidade especificada só poderá ser marcada como implementada quando
todos os seus critérios de aceitação forem validados.

## Alternativas consideradas

### Somente documentação clássica

Foi rejeitada como processo único porque explica bem o estado do sistema, mas
não estabelece uma relação explícita entre trabalho planejado, requisitos e
critérios de conclusão.

### Spec-driven para toda alteração

Foi rejeitada porque imporia custo desproporcional a correções editoriais,
renomeações e manutenção interna sem mudança de comportamento.

## Consequências

### Positivas

- O estado atual fica separado da intenção futura.
- Decisões permanecem consultáveis.
- Funcionalidades ganham critérios objetivos de conclusão.
- Colaboradores e agentes de IA recebem contexto mais preciso.

### Negativas

- Mudanças de comportamento exigem manutenção documental.
- Specs e documentos precisam ser revisados junto com o código.
- Será necessário evitar especificações detalhadas além do necessário.

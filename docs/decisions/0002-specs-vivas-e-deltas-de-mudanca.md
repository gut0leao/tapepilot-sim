# ADR 0002: Specs vivas e deltas de mudança

- **Estado:** Aceito
- **Data:** 2026-07-31
- **Substitui parcialmente:** ADR 0001

## Contexto

O processo inicial tratava cada funcionalidade futura como uma spec isolada e
mantinha o protótipo apenas na documentação clássica. Isso não garantia que todo
comportamento implementado estivesse coberto por requisitos formais.

Uma spec única do baseline resolveria a cobertura, mas perderia granularidade:
uma mudança de jitter, transporte ou visualização afetaria o mesmo documento.

## Decisão

O projeto adotará:

- specs vivas organizadas por capacidade, descrevendo o comportamento vigente;
- propostas de mudança separadas, contendo deltas sobre uma ou mais specs;
- incorporação do delta às specs depois da implementação e validação;
- arquivamento da proposta concluída para preservar contexto e evidências.

Correções que apenas restauram requisitos vigentes podem dispensar uma proposta,
mas devem referenciar os requisitos corrigidos.

## Consequências

### Positivas

- Todo comportamento atual pode ser rastreado a requisitos formais.
- Mudanças permanecem pequenas e focadas.
- As specs sempre descrevem o sistema vigente.
- O histórico de intenção permanece separado do contrato atual.

### Negativas

- Concluir uma mudança exige incorporar o delta e arquivar a proposta.
- Uma alteração transversal pode tocar várias specs.
- Índices e estados precisam permanecer sincronizados.


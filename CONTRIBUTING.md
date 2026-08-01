# Contribuindo com o TapePilot

## Preparação

Siga o [guia de desenvolvimento](docs/development.md) para criar o ambiente e
executar as verificações locais.

## Antes de modificar o código

Classifique a mudança:

| Mudança | Registro esperado |
|---|---|
| Correção editorial ou manutenção interna | descrição no commit/PR |
| Correção de comportamento especificado | referência ao requisito vigente |
| Nova funcionalidade ou mudança observável | proposta e delta |
| Mudança no modelo físico | proposta, delta e `simulation-model.md` |
| Decisão técnica duradoura | ADR |

Consulte as [specs de capacidade](docs/specs/README.md), o
[processo de mudanças](docs/changes/README.md) e os [ADRs](docs/decisions/README.md).
Para prioridade, sprint e estados do backlog, consulte o
[guia de gestão do projeto](docs/project-management.md).

## Implementação

- Preserve os requisitos vigentes, salvo quando uma proposta aprovada os
  alterar explicitamente.
- Mantenha o domínio testável sem Qt.
- Evite misturar refatoração ampla e mudança funcional no mesmo passo.
- Atualize documentos que tenham deixado de representar o sistema.

## Validação

```bash
python3 tools/check_docs.py
python3 -m unittest discover -v
python3 -m py_compile app.py sim/*.py tests/*.py tools/*.py
```

Quando o extra de desenvolvimento `.[dev]` estiver instalado:

```bash
python3 -m pytest
```

## Checklist de conclusão

- [ ] A mudança possui proposta aprovada ou dispensa proposta.
- [ ] Requisitos e critérios de aceitação foram verificados.
- [ ] Testes novos e existentes passam.
- [ ] Documentação clássica foi atualizada.
- [ ] Decisões duradouras possuem ADR.
- [ ] Deltas foram incorporados às specs afetadas.
- [ ] A proposta contém evidências e foi arquivada.
- [ ] Limitações remanescentes estão registradas.

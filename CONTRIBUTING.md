# Contribuindo com o TapePilot

## Preparação

Siga o [guia de desenvolvimento](docs/development.md) para criar o ambiente e
executar as verificações locais.

## Antes de modificar o código

Classifique a mudança:

| Mudança | Registro esperado |
|---|---|
| Correção editorial ou manutenção interna | descrição no commit/PR |
| Correção de comportamento especificado | referência ao requisito existente |
| Nova funcionalidade ou mudança observável | spec |
| Mudança no modelo físico | spec e `simulation-model.md` |
| Decisão técnica duradoura | ADR |

Consulte o [processo de especificações](docs/specs/README.md) e os
[ADRs](docs/decisions/README.md).

## Implementação

- Preserve o comportamento caracterizado, salvo quando uma spec aprovada o
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

- [ ] A mudança corresponde a uma spec aprovada ou dispensa spec.
- [ ] Requisitos e critérios de aceitação foram verificados.
- [ ] Testes novos e existentes passam.
- [ ] Documentação clássica foi atualizada.
- [ ] Decisões duradouras possuem ADR.
- [ ] A spec contém evidências e estado correto.
- [ ] Limitações remanescentes estão registradas.

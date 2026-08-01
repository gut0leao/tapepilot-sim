"""Valida links Markdown locais e a estrutura mínima das especificações."""

from pathlib import Path
import re
import sys
import unicodedata


ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")
REQUIRED_SPEC_SECTIONS = {
    "## Propósito",
    "## Escopo",
    "## Fora de escopo",
    "## Requisitos funcionais",
    "## Requisitos não funcionais",
    "## Critérios de aceitação",
    "## Limitações vigentes",
    "## Evidências",
}
REQUIRED_CHANGE_SECTIONS = {
    "## Problema",
    "## Objetivo",
    "## Fora de escopo",
    "## Impacto",
    "## Questões em aberto",
    "## Evidências de implementação",
}


def markdown_files():
    yield ROOT / "README.md"
    yield ROOT / "CONTRIBUTING.md"
    yield ROOT / "CHANGELOG.md"
    yield from sorted((ROOT / "docs").rglob("*.md"))


def heading_anchors(text):
    anchors = set()
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE):
        normalized = unicodedata.normalize("NFKD", heading)
        normalized = "".join(char for char in normalized if not unicodedata.combining(char))
        anchor = normalized.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"[\s_]+", "-", anchor).strip("-")
        occurrence = counts.get(anchor, 0)
        counts[anchor] = occurrence + 1
        if occurrence:
            anchor = f"{anchor}-{occurrence}"
        anchors.add(anchor)
    return anchors


def check_links(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    for raw_target in MARKDOWN_LINK.findall(text):
        raw_target = raw_target.strip()
        if "://" in raw_target or raw_target.startswith("mailto:"):
            continue
        target, separator, anchor = raw_target.partition("#")
        resolved = (path.parent / target).resolve() if target else path.resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: link inexistente: {target}")
            continue
        if separator and resolved.suffix == ".md":
            linked_text = resolved.read_text(encoding="utf-8")
            if anchor not in heading_anchors(linked_text):
                errors.append(
                    f"{path.relative_to(ROOT)}: âncora inexistente: {raw_target}"
                )
    return errors


def check_specs():
    errors = []
    requirement_locations = {}
    for path in sorted((ROOT / "docs/specs").glob("*/spec.md")):
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SPEC_SECTIONS:
            if section not in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: seção obrigatória ausente: {section}"
                )
        if not re.search(r"\*\*Estado:\*\* (Draft|Implemented|Superseded)", text):
            errors.append(f"{path.relative_to(ROOT)}: estado ausente ou inválido")
        for requirement_id in re.findall(r"\*\*([A-Z]{2}-(?:RF|RNF)-\d{2}):\*\*", text):
            requirement_locations.setdefault(requirement_id, []).append(path)
        for companion in ("design.md", "tasks.md"):
            if not (path.parent / companion).exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: arquivo obrigatório ausente: {companion}"
                )
    for requirement_id, paths in requirement_locations.items():
        if len(paths) > 1:
            locations = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"requisito duplicado {requirement_id}: {locations}")
    return errors


def check_changes():
    errors = []
    current_requirement_ids = set()
    for spec_path in sorted((ROOT / "docs/specs").glob("*/spec.md")):
        spec_text = spec_path.read_text(encoding="utf-8")
        current_requirement_ids.update(
            re.findall(r"\*\*([A-Z]{2}-(?:RF|RNF)-\d{2}):\*\*", spec_text)
        )
    added_requirement_locations = {}
    for path in sorted((ROOT / "docs/changes").glob("*/proposal.md")):
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_CHANGE_SECTIONS:
            if section not in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: seção obrigatória ausente: {section}"
                )
        if not re.search(
            r"\*\*Estado:\*\* (Draft|Approved|In Progress|Implemented|Rejected)",
            text,
        ):
            errors.append(f"{path.relative_to(ROOT)}: estado ausente ou inválido")
        for companion in ("spec-delta.md", "design.md", "tasks.md"):
            if not (path.parent / companion).exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: arquivo obrigatório ausente: {companion}"
                )
        delta_path = path.parent / "spec-delta.md"
        if delta_path.exists():
            delta_text = delta_path.read_text(encoding="utf-8")
            match = re.search(
                r"^## Requisitos adicionados\s*$([\s\S]*?)(?=^## |\Z)",
                delta_text,
                re.MULTILINE,
            )
            if match:
                for requirement_id in re.findall(
                    r"\*\*([A-Z]{2}-(?:RF|RNF)-\d{2}):\*\*", match.group(1)
                ):
                    added_requirement_locations.setdefault(requirement_id, []).append(
                        delta_path
                    )
    for requirement_id, paths in added_requirement_locations.items():
        if requirement_id in current_requirement_ids:
            locations = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(
                f"requisito futuro já existe nas specs vigentes {requirement_id}: "
                f"{locations}"
            )
        if len(paths) > 1:
            locations = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(
                f"requisito futuro duplicado {requirement_id}: {locations}"
            )
    return errors


def main():
    errors = []
    for path in markdown_files():
        errors.extend(check_links(path))
    errors.extend(check_specs())
    errors.extend(check_changes())

    if errors:
        print("Falhas na documentação:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentação validada com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

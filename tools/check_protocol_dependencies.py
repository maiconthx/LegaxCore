#!/usr/bin/env python3
"""Valida o snapshot de dependencias Bedrock contra o composer.lock e composer.json.

Este script NAO faz atualizacoes de protocolo, nao baixa codigos e nao atesta
compatibilidade com uma versao nova do Minecraft.
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_PACKAGES = {
    "pocketmine/bedrock-protocol",
    "pocketmine/bedrock-data",
    "pocketmine/bedrock-block-upgrade-schema",
    "pocketmine/bedrock-item-upgrade-schema",
}


def validate(root: Path) -> list[str]:
    manifest = json.loads((root / "legaxcore/dependency-pins.json").read_text(encoding="utf-8"))
    lock = json.loads((root / "composer.lock").read_text(encoding="utf-8"))
    composer = json.loads((root / "composer.json").read_text(encoding="utf-8"))
    errors = []
    packages = manifest.get("packages", [])
    names = [p.get("name") for p in packages]
    if len(names) != len(set(names)) or set(names) != REQUIRED_PACKAGES:
        errors.append("O manifesto deve conter exatamente as 4 bibliotecas Bedrock, sem duplicacoes.")
    if manifest.get("engine_baseline") != "5.44.3":
        errors.append("A versao-base declarada precisa ser 5.44.3.")

    locked = {pkg["name"]: pkg for pkg in lock.get("packages", [])}
    required = composer.get("require", {})
    for pin in packages:
        name = pin.get("name", "")
        current = locked.get(name)
        if current is None:
            errors.append(f"{name}: ausente do composer.lock")
            continue
        if name not in required:
            errors.append(f"{name}: ausente de composer.json")
        if current.get("version") != pin.get("version"):
            errors.append(f"{name}: versao do lock diferente da referencia validada")
        source = current.get("source") or {}
        if source.get("url") != pin.get("source_repo"):
            errors.append(f"{name}: origem Git alterada")
        if source.get("reference") != pin.get("source_reference"):
            errors.append(f"{name}: commit de origem Git alterado")
        if not re.fullmatch(r"[a-f0-9]{40}", str(pin.get("source_reference", ""))):
            errors.append(f"{name}: hash SHA-1 Git malformado")

    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    try:
        problems = validate(root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("ERRO: nao foi possivel verificar dependencias:", exc, file=sys.stderr)
        sys.exit(1)
    if problems:
        for problem in problems:
            print("ERRO:", problem, file=sys.stderr)
        sys.exit(1)
    print("Dependencias Bedrock fixadas e consistentes: 4/4. Nenhuma atualizacao aplicada.")

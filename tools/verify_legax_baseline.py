#!/usr/bin/env python3
"""Confirma a base PMMP 5.44.3; não certifica compatibilidade Bedrock futura."""
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

for file in ("composer.json", "composer.lock", "LICENSE", "src/VersionInfo.php",
             "build/server-phar.php", ".gitmodules", "legaxcore/compatibility.json",
             ".github/workflows/legax-ci.yml"):
    check((root / file).is_file(), f"Arquivo ausente: {file}")

manifest_path = root / "legaxcore/compatibility.json"
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    check(manifest.get("upstream", {}).get("tag") == "5.44.3", "Tag upstream diferente de 5.44.3")
    check(manifest.get("minecraft_bedrock", {}).get("supported_display_version") == "1.26.30",
          "Versão Bedrock original diferente de 1.26.30")
    check(manifest.get("engine_renamed_in_source") is False, "Renomeação prematura da engine")

version_info = root / "src/VersionInfo.php"
if version_info.is_file():
    source = version_info.read_text(encoding="utf-8")
    check(bool(re.search(r'const\s+BASE_VERSION\s*=\s*"5\.44\.3"', source)), "Versão base errada")
    check('public const NAME = "PocketMine-MP"' in source, "Nome da engine foi modificado")

composer_path = root / "composer.json"
if composer_path.is_file():
    composer = json.loads(composer_path.read_text(encoding="utf-8"))
    check(composer.get("name") == "pocketmine/pocketmine-mp", "Pacote Composer original alterado")
    required = composer.get("require", {})
    for package in ("pocketmine/bedrock-protocol", "pocketmine/bedrock-data", "ext-pmmpthread"):
        check(package in required, f"Dependência ausente: {package}")

if errors:
    for message in errors:
        print("ERRO:", message, file=sys.stderr)
    sys.exit(1)

print("Baseline OK: PocketMine-MP 5.44.3; Bedrock 1.26.30; API 5.")

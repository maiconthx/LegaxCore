#!/usr/bin/env bash
set -Eeuo pipefail

# Uso em GitHub Actions; requer GH_TOKEN com permissão issues:write.
# Consulta a documentacao PUBLICADA, sem baixar conteudo sob licenca Mojang.
: "${GH_TOKEN:?Defina GH_TOKEN}"
: "${GH_REPO:?Defina GH_REPO no formato owner/repo}"

tag="$(gh api repos/Mojang/bedrock-protocol-docs/releases/latest --jq '.tag_name')"
if [[ ! "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+([-.][A-Za-z0-9.-]+)?$ ]]; then
  echo "Tag da Mojang inesperada: $tag" >&2
  exit 1
fi

title="[Bedrock Docs] Analisar ${tag}"
export LEGAX_ISSUE_TITLE="$title"

# Dedupe exato pela title (sem criar uma nova issue em todas as execucoes).
existing="$(gh issue list --repo "$GH_REPO" --state all --limit 500 --json title | python3 -c '
import json,os,sys
issues=json.load(sys.stdin)
print("yes" if any(x.get("title")==os.environ["LEGAX_ISSUE_TITLE"] for x in issues) else "no")
')"

if [[ "$existing" == yes ]]; then
  echo "Issue ja registrada: $title"
  exit 0
fi

body="Foi publicada a versao ${tag} dos documentos oficiais do protocolo Bedrock.

Origem: https://github.com/Mojang/bedrock-protocol-docs/releases/tag/${tag}

Checklist:
- [ ] Comparar pacotes, enums, campos e mudancas de tipos
- [ ] Verificar disponibilidade dos dados de blocos, itens e biomas
- [ ] Planejar alteracoes em LegaxProtocol e LegaxData
- [ ] Validar testes de serializacao e handshake/login com cliente real
- [ ] Testar BedWars, SkyWars, inventario e mundos antes de anunciar compatibilidade

**Aviso:** a criacao desta issue NAO significa que o LegaxCore suporta esta versao. Nao publicar automaticamente."
gh issue create --repo "$GH_REPO" --title "$title" --body "$body"

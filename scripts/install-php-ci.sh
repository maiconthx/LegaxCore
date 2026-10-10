#!/usr/bin/env bash
set -Eeuo pipefail

# Runner Linux x86_64. Usa PHP 8.2 oficial de PMMP 5, validado por SHA-256.
if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
  echo "Este script requer Linux x86_64" >&2
  exit 1
fi

INSTALL_ROOT="${RUNNER_TEMP:-${TMPDIR:-/tmp}}/legax-php"
mkdir -p "$INSTALL_ROOT"
ARCHIVE="$INSTALL_ROOT/php-pmmp.tar.gz"
URL='https://github.com/pmmp/PHP-Binaries/releases/download/pm5-php-8.2-latest/PHP-8.2-Linux-x86_64-PM5.tar.gz'
SHA256='000fc605878d24be3d6faa6991c0d3a39ae90a0f9ff24d9f4e4722ef823082fc'

curl --fail --location --silent --show-error --retry 3 "$URL" --output "$ARCHIVE"
echo "$SHA256  $ARCHIVE" | sha256sum --check --status || {
  echo "SHA-256 inválido; não executar binário" >&2
  exit 1
}
tar -xzf "$ARCHIVE" -C "$INSTALL_ROOT"

PHP_BIN_DIR="$INSTALL_ROOT/bin/php7/bin"
PHP_BIN="$PHP_BIN_DIR/php"
PHP_INI="$PHP_BIN_DIR/php.ini"
test -x "$PHP_BIN" || { echo "PHP PMMP não encontrado" >&2; exit 1; }

EXT_PARENT="$INSTALL_ROOT/bin/php7/lib/php/extensions"
if [[ -d "$EXT_PARENT" ]]; then
  EXT_DIR="$(find "$EXT_PARENT" -mindepth 1 -maxdepth 1 -type d -name '*debug-zts*' -print -quit)"
  if [[ -n "$EXT_DIR" && -f "$PHP_INI" ]]; then
    python3 - "$PHP_INI" "$EXT_DIR" <<'PY'
from pathlib import Path
import re
import sys
p = Path(sys.argv[1])
ext = sys.argv[2]
raw = p.read_text(encoding="utf-8")
raw = re.sub(r'^\s*extension_dir\s*=.*$', '', raw, flags=re.MULTILINE)
p.write_text(raw.rstrip() + '\n' + 'extension_dir="' + ext + '"\n', encoding="utf-8")
PY
  fi
fi

curl --fail --location --silent --show-error --retry 3 \
  'https://getcomposer.org/download/latest-2.x/composer.phar' \
  --output "$PHP_BIN_DIR/composer.phar"
cat > "$PHP_BIN_DIR/composer" <<'WRAPPER'
#!/usr/bin/env bash
set -e
exec "$(dirname "$0")/php" "$(dirname "$0")/composer.phar" "$@"
WRAPPER
chmod +x "$PHP_BIN_DIR/composer"

if [[ -n "${GITHUB_PATH:-}" ]]; then
  echo "$PHP_BIN_DIR" >> "$GITHUB_PATH"
else
  echo "Adicione ao PATH: $PHP_BIN_DIR"
fi
"$PHP_BIN" -v
"$PHP_BIN" -r 'foreach (["pmmpthread", "chunkutils2", "leveldb"] as $e) { if (!extension_loaded($e)) { fwrite(STDERR, "Extensão ausente: $e\n"); exit(1); } } echo "Extensões essenciais OK\n";'
"$PHP_BIN_DIR/composer" --version

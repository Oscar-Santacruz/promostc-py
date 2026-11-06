#!/usr/bin/env python3
"""Checks del sitio estático: referencias locales rotas, HTML balanceado y datos JSON.

No revisa links externos: Instagram/Facebook bloquean bots y darían falsos rojos.
Uso: python3 .github/scripts/check_site.py [raíz]  (sale con 1 si hay errores).
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# html, head y body tienen apertura y cierre opcionales en HTML5: no se balancean.
OPTIONAL = {"html", "head", "body"}
VOID = OPTIONAL | {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}
# Paraguay con margen: atrapa lat/lon invertidas o coordenadas de otro país.
LAT, LON = (-28.0, -19.0), (-63.0, -54.0)


def is_local(ref):
    ref = ref.strip()
    if not ref or "${" in ref:  # vacío o template de JS
        return False
    return not re.match(r"^([a-z][a-z0-9+.-]*:|//|#)", ref, re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.stack, self.errors = [], [], []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value and is_local(value):
                self.refs.append(value)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            open_tag = self.stack[-1] if self.stack else None
            self.errors.append(f"línea {self.getpos()[0]}: </{tag}> no cierra {open_tag}")
            # Recupera: saca hasta encontrar la etiqueta, si está abierta.
            if any(t == tag for t, _ in self.stack):
                while self.stack.pop()[0] != tag:
                    pass
            return
        self.stack.pop()


def main(root):
    errors = []
    html = (root / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(html)
    page.close()
    errors += page.errors
    errors += [f"<{t}> de la línea {n} sin cerrar" for t, n in page.stack]

    refs = set(page.refs) | set(re.findall(r"""fetch\(\s*["']([^"']+)["']""", html))
    refs |= set(re.findall(r"""["'`](logos/[^"'`$]+\.(?:svg|png|jpg|webp|json))["'`]""", html))
    for ref in sorted(r for r in refs if is_local(r)):
        path = ref.split("#")[0].split("?")[0]
        if path and not (root / path).is_file():
            errors.append(f"referencia rota: {ref}")

    try:
        stations = json.loads((root / "stations.json").read_text(encoding="utf-8"))
        for i, row in enumerate(stations):
            ok = (isinstance(row, list) and len(row) == 5
                  and all(isinstance(v, (int, float)) for v in row[:2])
                  and isinstance(row[2], (str, type(None)))  # emblema: null si no tiene
                  and isinstance(row[3], str)
                  and isinstance(row[4], (str, type(None))))
            if not ok:
                errors.append(f"stations.json[{i}]: forma inválida {row!r}")
            elif not (LAT[0] <= row[0] <= LAT[1] and LON[0] <= row[1] <= LON[1]):
                errors.append(f"stations.json[{i}]: fuera de Paraguay {row[:2]}")
    except ValueError as exc:
        errors.append(f"stations.json no es JSON válido: {exc}")

    try:
        logos = json.loads((root / "logos" / "logos.json").read_text(encoding="utf-8"))
        for slug, logo in logos.items():
            for key in ("icon", "logo"):
                if logo.get(key) and not (root / logo[key]).is_file():
                    errors.append(f"logos.json {slug}.{key}: falta {logo[key]}")
    except ValueError as exc:
        errors.append(f"logos.json no es JSON válido: {exc}")

    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(refs)} referencias locales, {len(errors)} errores")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))

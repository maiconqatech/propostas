#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de propostas.

Le a planilha mestre de leads (leads/leads-sem-site.csv), filtra por nicho,
e gera uma pasta por lead com um index.html pronto (auto-contido) + dados.json.

Rodar de novo sobrescreve tudo: os templates das 5 landing pages sao a fonte
da verdade. Para atualizar todas as propostas, edite o template e rode:

    python gerar.py

Saida:
    <nicho>/<slug>/index.html   pagina pronta pra mandar no WhatsApp
    <nicho>/<slug>/dados.json   dados do lead (pra editar/consulta)
    <nicho>/_INDICE.md          lista slug -> url -> whatsapp (rastreio de abordagem)
    <nicho>/_leads.csv          mesmo conteudo em csv
"""
import csv, json, re, unicodedata, pathlib, sys

RAIZ = pathlib.Path(__file__).parent
CSV_MESTRE = RAIZ / "leads" / "leads-sem-site.csv"

USUARIO_GH = "maiconqatech"
REPO = "propostas"

# base das URLs das propostas.
#   com dominio proprio ligado no repo:  "https://lancaseusite.com.br"
#   sem dominio (github pages padrao):   f"https://{USUARIO_GH}.github.io/{REPO}"
BASE = "https://lancaseusite.com.br"

TPL = RAIZ / "_templates"

# nicho -> (template, marca generica do template, mensagem padrao do WhatsApp)
NICHOS = {
    "odonto": {
        "template": TPL / "odonto.html",
        "marca": "Sorriso Odontologia",
        "msg": "Olá! Vim pelo site e gostaria de agendar uma avaliação.",
    },
    "vet": {
        "template": TPL / "vet.html",
        "marca": "Vida Animal",
        "msg": "Olá! Vim pelo site e gostaria de agendar um horário para o meu pet.",
    },
    "fisio": {
        "template": TPL / "fisio.html",
        "marca": "Reabilita Fisioterapia",
        "msg": "Olá! Vim pelo site e gostaria de agendar uma avaliação de fisioterapia.",
    },
    "pilates": {
        "template": TPL / "pilates.html",
        "marca": "Núcleo Pilates",
        "msg": "Olá! Vim pelo site e gostaria de agendar uma aula experimental de pilates.",
    },
    "auto": {
        "template": TPL / "auto.html",
        "marca": "Studio Detail",
        "msg": "Olá! Vim pelo site e gostaria de um orçamento de estética automotiva.",
    },
}

_MIN = {"de", "da", "do", "das", "dos", "e", "em", "a", "o"}


def titulo(nome: str) -> str:
    """Se o nome vier todo em CAIXA ALTA, deixa em Caixa de Titulo."""
    if not nome or any(c.islower() for c in nome):
        return nome
    out = []
    for w in nome.split():
        lw = w.lower()
        out.append(lw if lw in _MIN and out else lw.capitalize())
    return " ".join(out)


def sa(s: str) -> str:
    """sem acento, minusculo, trim"""
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower().strip()


def casa(nicho: str, cat: str, setor: str, nome: str) -> bool:
    c, s, n = sa(cat), sa(setor), sa(nome)
    if nicho == "odonto":
        return s == "odontologia" or "dentista" in c or "odontolog" in c
    if nicho == "vet":
        return "veterinar" in c
    if nicho == "fisio":
        return "fisioterap" in c
    if nicho == "pilates":
        return "pilates" in c
    if nicho == "auto":
        return any(k in c for k in ["lava-rapido", "lava rapido", "pintura automotiva", "martelinho", "estetica automotiv"]) \
            or any(k in n for k in ["estetica automotiv", "detail", "polimento", "higienizacao automotiva"])
    return False


def slug(nome: str, gmaps: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", sa(nome)).strip("-")[:48].strip("-")
    m = re.search(r"(\d{3,})", gmaps or "")
    suf = m.group(1)[-4:] if m else "0000"
    return f"{base}-{suf}"


def so_digitos(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def monta_config(lead: dict, nicho: str) -> dict:
    cidade = lead["Cidade"].strip()
    endereco = lead["Endereco"].strip()
    endereco_full = f"{endereco}, {cidade} - SP" if endereco else f"{cidade} - SP"
    wa = so_digitos(lead["WhatsApp"] or lead["Telefone"])
    if wa and not wa.startswith("55"):
        wa = "55" + wa
    return {
        "nome": titulo(lead["Nome"].strip()),
        "whatsapp": wa,
        "telefone": lead["Telefone"].strip() or "(00) 00000-0000",
        "endereco": endereco_full,
        "instagram": "",
        "msgPadrao": NICHOS[nicho]["msg"],
    }


RE_CONFIG = re.compile(r"const CONFIG = \{.*?\};", re.S)


def renderiza(tpl: str, cfg: dict, nota: str, aval: str, marca: str) -> str:
    nome = cfg["nome"]
    # troca a marca generica do template pelo nome do lead (logo, title, textos, rodape)
    html = tpl.replace(marca, nome).replace(marca.replace(" ", "&nbsp;"), nome)

    novo_cfg = "const CONFIG = " + json.dumps(cfg, ensure_ascii=False, indent=2) + ";"
    html = RE_CONFIG.sub(lambda _: novo_cfg, html, count=1)

    # nao indexar no google
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex, nofollow">',
        1,
    )

    # nota real do google
    tem_nota = bool(nota) and nota not in ("0", "0,0", "0.0")
    tem_aval = bool(aval) and aval.isdigit() and int(aval) >= 3
    if tem_nota:
        html = html.replace("<b>4,9</b> de 5 no Google", f"<b>{nota}</b> de 5 no Google")
        html = html.replace(">4,9 ★<", f">{nota} ★<")
        html = html.replace('"big">4,9★<', f'"big">{nota}★<')
        if tem_aval:
            html = html.replace("+45 avaliações", f"{aval} avaliações")
        else:
            html = html.replace("no Google, +45 avaliações", "no Google")
            html = html.replace(" · +45 avaliações", "")
            html = html.replace("+45 avaliações", "no Google")
    else:
        # sem nota real: remove qualquer alegacao de avaliacao do template
        html = re.sub(r'<div><span class="num">4,9 ★</span><span class="lbl">[^<]*</span></div>\s*', "", html)
        html = re.sub(r'<div class="rating-line">.*?</div>\s*', "", html, flags=re.S)
        html = re.sub(r'<div class="badge">.*?</div>\s*', "", html, flags=re.S)

    # esconde botoes/links de instagram (nao temos o @ do lead)
    html = html.replace(
        "</body>",
        "<script>try{if(typeof CONFIG==='undefined'||!CONFIG.instagram){"
        "document.querySelectorAll('[data-instagram]').forEach(function(e){e.style.display='none'});}}catch(_){}</script>\n</body>",
        1,
    )
    return html


def main():
    if not CSV_MESTRE.exists():
        sys.exit(f"nao achei {CSV_MESTRE}")
    leads = list(csv.DictReader(open(CSV_MESTRE, encoding="utf-8-sig"), delimiter=";"))

    resumo = {}
    for nicho, meta in NICHOS.items():
        tpl_path = meta["template"]
        if not tpl_path.exists():
            print(f"  ! template ausente para {nicho}: {tpl_path}")
            continue
        tpl = tpl_path.read_text(encoding="utf-8")

        selec = [l for l in leads if casa(nicho, l["Categoria"], l["Setor"], l["Nome"])]
        indice = []
        vistos = set()
        for lead in selec:
            sl = slug(lead["Nome"], lead["GoogleMaps"])
            while sl in vistos:
                sl += "x"
            vistos.add(sl)

            cfg = monta_config(lead, nicho)
            nota = (lead["Nota"] or "").strip()
            aval = (lead["Avaliacoes"] or "").strip()

            pasta = RAIZ / nicho / sl
            url = f"{BASE}/{nicho}/{sl}/"

            # pagina feita a mao (arquivo .manual na pasta): nao sobrescreve, so registra no indice
            if (pasta / ".manual").exists():
                indice.append({
                    "slug": sl, "nome": lead["Nome"].strip(), "cidade": lead["Cidade"].strip(),
                    "whatsapp": cfg["whatsapp"], "telefone": cfg["telefone"],
                    "nota": nota, "avaliacoes": aval, "url": url, "status": "manual",
                })
                continue

            html = renderiza(tpl, cfg, nota, aval, meta["marca"])
            pasta.mkdir(parents=True, exist_ok=True)
            (pasta / "index.html").write_text(html, encoding="utf-8")
            (pasta / "dados.json").write_text(
                json.dumps(
                    {
                        "nome": lead["Nome"].strip(),
                        "cidade": lead["Cidade"].strip(),
                        "categoria": lead["Categoria"].strip(),
                        "endereco": cfg["endereco"],
                        "telefone": cfg["telefone"],
                        "whatsapp": cfg["whatsapp"],
                        "nota_google": nota,
                        "avaliacoes_google": aval,
                        "google_maps": lead["GoogleMaps"].strip(),
                        "config": cfg,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            indice.append(
                {
                    "slug": sl,
                    "nome": lead["Nome"].strip(),
                    "cidade": lead["Cidade"].strip(),
                    "whatsapp": cfg["whatsapp"],
                    "telefone": cfg["telefone"],
                    "nota": nota,
                    "avaliacoes": aval,
                    "url": url,
                    "status": "",
                }
            )

        # _INDICE.md
        md = [f"# Propostas - {nicho}", "", f"{len(indice)} leads.  Status: (vazio) nao enviado | enviado | respondeu | fechou | descartar", ""]
        md.append("| Empresa | Cidade | WhatsApp | Nota | Link | Status |")
        md.append("|---|---|---|---|---|---|")
        for r in indice:
            md.append(f"| {r['nome']} | {r['cidade']} | {r['whatsapp']} | {r['nota']} ({r['avaliacoes']}) | {r['url']} | {r['status']} |")
        (RAIZ / nicho).mkdir(parents=True, exist_ok=True)
        (RAIZ / nicho / "_INDICE.md").write_text("\n".join(md) + "\n", encoding="utf-8")

        # _leads.csv
        with open(RAIZ / nicho / "_leads.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["slug", "nome", "cidade", "whatsapp", "telefone", "nota", "avaliacoes", "url", "status"], delimiter=";")
            w.writeheader()
            w.writerows(indice)

        resumo[nicho] = len(indice)
        print(f"  {nicho:8s} {len(indice):4d} propostas")

    print("\n  total:", sum(resumo.values()))
    print("  regerar: python gerar.py")


if __name__ == "__main__":
    main()

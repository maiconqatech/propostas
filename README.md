# Propostas

Páginas de prospecção geradas em lote, uma por lead, a partir dos 5 templates de nicho.
Cada página já vem com o nome, endereço, telefone e nota do Google do lead. É só mandar o link no WhatsApp.

## Estrutura

```
propostas/
  gerar.py                 gerador
  leads/leads-sem-site.csv  planilha mestre (todos os leads da região, sem site)
  _templates/               os 5 templates (fonte da verdade)
    odonto.html  vet.html  fisio.html  pilates.html  auto.html
  odonto/
    _INDICE.md              lista: empresa | whatsapp | link | status  (rastreio da abordagem)
    _leads.csv              mesma coisa em csv
    <slug>/
      index.html            página pronta (auto-contida)
      dados.json            dados do lead
  vet/  fisio/  pilates/  auto/   (mesma estrutura)
```

## Fluxo de uso

1. **Gerar / regerar tudo:**
   ```
   python gerar.py
   ```
   Sobrescreve todas as pastas de nicho a partir dos templates + da planilha.
   Editou um template? Roda de novo e todas as propostas daquele nicho atualizam.

2. **Publicar:** `git add -A && git commit -m "..." && git push`
   As páginas ficam em `https://maiconqatech.github.io/propostas/<nicho>/<slug>/`

3. **Abordar:** abra `<nicho>/_INDICE.md`, pegue os links, mande no WhatsApp seguindo a
   estratégia (arquivo `estrategia-whatsapp` na pasta Produtos). Marque o status na coluna.

4. **Personalizar quem respondeu:** edite o `index.html` daquele lead (trocar fotos do
   Unsplash pelas reais, colocar avaliações reais do Google, ajustar textos).

5. **Faxina semanal:** apague as pastas de quem não respondeu em 30 dias e faça commit.
   Para recriar do zero, é só rodar `gerar.py` de novo.

## O que já vem preenchido

- Nome do negócio (logo, título da aba, textos, rodapé)
- Telefone e WhatsApp (todos os botões e o formulário caem no número do lead)
- Endereço + mapa do Google
- Nota e número de avaliações do Google (real). Sem nota no cadastro, os blocos de
  avaliação são removidos da página, nada de nota falsa.
- `noindex` no `<head>`: as páginas não aparecem no Google.

## O que falta personalizar (só depois que o lead responder)

- Fotos (estão com placeholder do Unsplash)
- Textos dos depoimentos (há 3 genéricos + nota "troque pelos reais")
- Instagram (não temos o @ no cadastro; os botões de Instagram ficam ocultos)
- Lista de serviços / horário (estão no padrão do nicho)

## Nichos e volume

| Nicho | Pasta | Leads |
|---|---|---|
| Odontologia | `odonto/` | 118 |
| Veterinária | `vet/` | 70 |
| Fisioterapia | `fisio/` | 71 |
| Estética automotiva | `auto/` | 36 |
| Estúdio de pilates | `pilates/` | 10 |

Fonte: `leads/leads-sem-site.csv` (2110 negócios da região sem site; o gerador filtra por categoria).

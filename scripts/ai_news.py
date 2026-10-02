"""Manchetes de IA / big techs (Google News RSS, sem login). Uso: python scripts/ai_news.py [horas=6]
Mostra horario BRT, fonte e titulo, mais recentes primeiro. Fonte = agregador: horario vem do RSS (pubDate).
ponytail: so Google News RSS; adicionar X/Reddit/RSS oficiais das empresas quando precisar de mais cobertura."""
import sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

QUERIES = ["OpenAI ChatGPT", "Nvidia AI chips", "Meta AI Llama", "xAI Grok Musk", "Anthropic Claude",
           "Google Gemini", "Microsoft Copilot AI", "AI data center capex", "AI bubble stocks"]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # console Windows cp1252 quebra com manchetes
hours = float(sys.argv[1]) if len(sys.argv) > 1 else 6
BRT = timezone(timedelta(hours=-3))
since = datetime.now(timezone.utc) - timedelta(hours=hours)
seen, items = set(), []
for q in QUERIES:
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(q + f" when:{int(max(1, hours))}h") + "&hl=en-US&gl=US&ceid=US:en"
    try:
        root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=15).read())
    except Exception as e:
        print(f"[erro {q}: {e}]"); continue
    for it in root.iter("item"):
        t = it.findtext("title"); d = parsedate_to_datetime(it.findtext("pubDate"))
        if t in seen or d < since: continue
        seen.add(t); items.append((d, q, t))
for d, q, t in sorted(items, reverse=True)[:40]:
    print(f"{d.astimezone(BRT):%d/%m %H:%M} [{q.split()[0]}] {t}")
print(f"-- {len(items)} manchetes unicas nas ultimas {hours:g} h")

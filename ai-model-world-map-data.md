# AI Model World Map — Data Table

Companion data for `ai-model-world-map.html`. **46 models, prices from OpenRouter `/api/v1/models` (July 2026).**
Position on the map = **origin (lab HQ)** · size = **estimated model scale** · colour = **output cost**.

**Prices are for hosted inference on OpenRouter.** Open-weight (✅) models are only "free" if you self-host them yourself; via an API you still pay a serving fee. Models marked **not on OR** (image generators, translation engines, and sovereign/enterprise direct-API labs) are not listed on OpenRouter, so they carry no per-token price here — that is why several European and Middle-East entries have no figures.

| # | Lab | Modell | Open? | Kap. | In $/M | Out $/M | Kontext | Herkunft (HQ) | Hosting | OR? |
|---|-----|--------|:-----:|:----:|:------:|:-------:|:-------:|:-------------:|:-------:|:---:|
| 1 | OpenAI | GPT-5.5 Pro | ❌ | Frontier | $30 | $180 | 1.05M | San Francisco, US | US | ✅ |
| 2 | OpenAI | GPT-5.5 | ❌ | Frontier | $5 | $30 | 1.05M | San Francisco, US | US | ✅ |
| 3 | Anthropic | Claude Fable 5 | ❌ | Frontier | $10 | $50 | 1M | San Francisco, US | US | ✅ |
| 4 | Anthropic | Claude Opus 4.8 | ❌ | Frontier | $5 | $25 | 1M | San Francisco, US | US | ✅ |
| 5 | Anthropic | Claude Sonnet 5 | ❌ | Strong | $2 | $10 | 1M | San Francisco, US | US | ✅ |
| 6 | Google | Gemini 3 Pro | ❌ | Frontier | $2 | $12 | 1.05M | Mountain View, US | US | ✅ |
| 7 | Google | Gemini 3.5 Flash | ❌ | Strong | $1.50 | $9 | 1.05M | Mountain View, US | US | ✅ |
| 8 | Google | Gemma 4 26B | ✅ | Mid | $0.06 | $0.33 | 262K | Mountain View, US | anywhere | ✅ |
| 9 | Meta | Llama 4 Maverick | ✅ | Strong | $0.15 | $0.60 | 1.05M | Menlo Park, US | anywhere | ✅ |
| 10 | xAI | Grok 4.3 | ❌ | Frontier | $1.25 | $2.50 | 1M | San Francisco, US | US | ✅ |
| 11 | Perplexity | Sonar Pro Search | ❌ | Specialist | $3 | $15 | 200K | San Francisco, US | US | ✅ |
| 12 | Writer | Palmyra X5 | ❌ | Strong | $0.60 | $6 | 1.04M | San Francisco, US | US | ✅ |
| 13 | Inflection | Inflection 3 | ❌ | Strong | $2.50 | $10 | 8K | Palo Alto, US | US | ✅ |
| 14 | Nvidia | Nemotron 3 Ultra 550B | ✅ | Strong | $0.50 | $2.20 | 1M | Santa Clara, US | anywhere | ✅ |
| 15 | AI2 (Allen) | OLMo 3 32B Think | ✅ | Mid | $0.15 | $0.50 | 65K | Seattle, US | anywhere | ✅ |
| 16 | Microsoft | Phi-4 | ✅ | Mid | $0.07 | $0.14 | 16K | Redmond, US | anywhere | ✅ |
| 17 | IBM | Granite 4.1 8B | ✅ | Mid | $0.05 | $0.10 | 131K | US | anywhere | ✅ |
| 18 | Liquid | LFM 2 24B | ✅ | Mid | $0.03 | $0.12 | 128K | NYC / Zürich | anywhere | ✅ |
| 19 | Nous Research | Hermes 4 405B | ✅ | Strong | $1 | $3 | 131K | Remote / US | anywhere | ✅ |
| 20 | Cohere | Command A | ❌ | Strong | $2.50 | $10 | 256K | Toronto, CA | US | ✅ |
| 21 | Mistral AI | Mistral Large 2512 | ✅ | Strong | $0.50 | $1.50 | 262K | Paris, FR | EU / US | ✅ |
| 22 | Mistral AI | Mistral Medium 3.5 | ❌ | Strong | $1.50 | $7.50 | 262K | Paris, FR | EU / US | ✅ |
| 23 | DeepCogito | Cogito V2.1 671B | ✅ | Strong | $1.25 | $1.25 | 128K | Paris / US | EU / US | ✅ |
| 24 | Poolside | Laguna XS.2 | ❌ | Strong | $0.10 | $0.20 | 262K | Paris / SF | EU / US | ✅ |
| 25 | Reka AI | Reka Edge | ✅ | Mid | $0.10 | $0.10 | 16K | London, UK | anywhere | ✅ |
| 26 | Aleph Alpha | Luminous / Pharia | ❌ | Strong | — | — | — | Heidelberg, DE | DE (direct API) | ❌ nicht auf OR (Sovereign) |
| 27 | LightOn | Paradigm | ❌ | Mid | — | — | — | Paris, FR | FR (direct API) | ❌ nicht auf OR (Enterprise) |
| 28 | DeepL | DeepL Translate | ❌ | Specialist | — | — | — | Cologne, DE | DE (direct API) | ❌ nicht auf OR (Übersetzung) |
| 29 | Stability AI | Stable Diffusion | ✅ | Specialist | — | — | — | London, UK | anywhere | ❌ nicht auf OR (Bild) |
| 30 | Black Forest Labs | Flux | ✅ | Specialist | — | — | — | Stuttgart / Berlin, DE | anywhere | ❌ nicht auf OR (Bild) |
| 31 | DeepSeek | DeepSeek V4 Pro | ✅ | Frontier | $0.43 | $0.87 | 1.05M | Hangzhou, CN | **CN + US/EU** | ✅ |
| 32 | Qwen (Alibaba) | Qwen 3.7 Plus | ✅ | Frontier | $0.32 | $1.28 | 1M | Hangzhou, CN | **CN + US/EU** | ✅ |
| 33 | Z.AI (Zhipu) | GLM 5.2 | ✅ | Frontier | $0.93 | $3 | 1.05M | Beijing, CN | **CN + US/EU** | ✅ |
| 34 | Baidu | ERNIE 4.5 VL | ✅ | Strong | $0.42 | $1.25 | 131K | Beijing, CN | **CN + US/EU** | ✅ |
| 35 | Moonshot AI | Kimi K2.7 | ❌ | Frontier | $0.74 | $3.50 | 262K | Beijing, CN | CN | ✅ |
| 36 | MiniMax | MiniMax M3 | ❌ | Strong | $0.30 | $1.20 | 1.05M | Shanghai, CN | CN | ✅ |
| 37 | Tencent | Hunyuan 3 | ❌ | Strong | $0.06 | $0.21 | 262K | Shenzhen, CN | CN | ✅ |
| 38 | ByteDance | Seed 2.0 | ❌ | Strong | $0.25 | $2 | 262K | Beijing, CN | CN | ✅ |
| 39 | StepFun | Step 3.7 Flash | ❌ | Mid | $0.20 | $1.15 | 256K | Beijing, CN | CN | ✅ |
| 40 | Xiaomi | MiMo v2.5 Pro | ❌ | Strong | $0.43 | $0.87 | 1.05M | Beijing, CN | CN | ✅ |
| 41 | AI21 | Jamba Large 1.7 | ❌ | Strong | $2 | $8 | 256K | Tel Aviv, IL | US / IL | ✅ |
| 42 | Sakana AI | Fugu Ultra | ❌ | Specialist | $5 | $30 | 1M | Tokyo, JP | JP | ✅ |
| 43 | Upstage | Solar Pro 3 | ✅ | Mid | $0.15 | $0.60 | 128K | Seongnam, KR | KR / US | ✅ |
| 44 | TII | Falcon H2 | ✅ | Strong | — | — | 262K | Abu Dhabi, AE | anywhere | ❌ nicht auf OR (Direct API) |
| 45 | G42 | Jais 2 | ✅ | Mid | — | — | 131K | Abu Dhabi, AE | anywhere | ❌ nicht auf OR (Direct API) |
| 46 | SDAIA | ALLaM 2 | ❌ | Mid | — | — | 131K | Riyadh, SA | SA (watsonx) | ❌ nicht auf OR (Direct API) |

## Kapabilität (Größe der Punkte = geschätzte Modellgröße)

| Tier | Bedeutung | Beispiele |
|------|-----------|-----------|
| **Frontier** | Flaggschiff-Reasoning, top-tier | GPT-5.5 Pro, Claude Fable 5, Grok 4.3, DeepSeek V4 Pro, Qwen 3.7, GLM 5.2, Kimi K2.7 |
| **Strong** | Leistungsstarke Arbeitspferde | Sonnet 5, Llama 4, Nemotron Ultra, Mistral Large/Medium, Hermes 4, ERNIE, Hunyuan, Falcon |
| **Mid** | Klein / effizient / Edge | Gemma 4, Phi-4, Granite, OLMo, LFM 2, Solar Pro, Reka Edge |
| **Specialist** | Bild / Übersetzung / Suche / Agent | Flux, Stable Diffusion, DeepL, Sonar Pro, Fugu Ultra |

## Farbskala (Output $/M)

| Farbe | Kosten | Beispiele |
|-------|--------|-----------|
| 🟢 Grün | < $1 | Hunyuan ($0.21), DeepSeek ($0.87), Gemma 4 ($0.33), Solar Pro ($0.60) |
| 🟡 Gelbgrün | $1 – $5 | Mistral Large ($1.50), Qwen 3.7 ($1.28), Grok 4.3 ($2.50), GLM 5.2 ($3), Kimi ($3.50) |
| 🟠 Orange | $5 – $15 | Palmyra X5 ($6), Mistral Medium ($7.50), Jamba ($8), Command A / Sonnet 5 ($10), Sonar ($15) |
| 🔴 Rot | $15 – $50 | Claude Opus 4.8 ($25), Fugu Ultra ($30), Claude Fable 5 ($50) |
| 🟥 Dunkelrot | > $50 | GPT-5.5 ($30 out on base, $180 on Pro) — **GPT-5.5 Pro ($180)** |
| ⚪ Grau | nicht Token-bepreist / nicht auf OR | Luminous, LightOn, DeepL, Stable Diffusion, Flux, Falcon, Jais, ALLaM |

## Herkunft vs. Hosting — der Kernpunkt

- **Offene Modelle** (● gefüllt) sind selbst hostbar. Offene chinesische Modelle (DeepSeek, Qwen, GLM, ERNIE 4.5) laufen problemlos auf US-/EU-Infrastruktur (Together, DeepInfra, Nebius, OVHcloud, Scaleway) — die Daten müssen China nicht erreichen. Der gestrichelte Bogen auf der Karte zeigt diesen West-Hosting-Pfad.
- **Geschlossene Modelle** (◌ Ring) binden an die Serving-Region des Labors. Ein geschlossenes chinesisches Modell (Kimi, MiniMax, Hunyuan, Seed, Step, MiMo) bedeutet: die Anfragen gehen nach China. Kein Bogen.

## Middle East

Die Golf-Staaten sind noch nicht auf Frontier-Niveau. **VAE** ist der reale Akteur: TII (Falcon, offen) und G42 (Jais, arabisch, offen). **Saudi-Arabien** investiert massiv (HUMAIN/PIF), hat aber mit ALLaM bisher kein Frontier-Modell. Keines dieser Modelle ist auf OpenRouter.

## Quellen

- OpenRouter API `/api/v1/models` (Juli 2026): 338 Modelle von 50+ Labs
- Herkunft = Lab-HQ; Hosting = bekannte Inference-Provider (inkl. EU: Nebius, OVHcloud, Scaleway)
- Open/Closed nach Modell-Lizenz; Kapabilität + Modellgröße = Einordnung/Schätzung, keine Benchmark-Rangliste

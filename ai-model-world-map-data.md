# AI Model World Map — Data Table

Position on the map = **origin (lab HQ)**. Size = **estimated model scale (parameters)**. Colour = **output cost**.
Filled dot = **open weights**, ring = **closed**. A dashed arc marks an open model that is
routinely **hostable in the West** even though its origin is elsewhere.

| # | Lab | Modell | Open? | Kapabilität | Input $/M | Output $/M | Kontext | Parameter | Herkunft (HQ) | Hosting (Serving) | Auf OR? |
|---|-----|--------|:-----:|:-----------:|:---------:|:----------:|:-------:|:---------:|:-------------:|:-----------------:|:-------:|
| 1 | OpenAI | GPT-5.4 Pro | ❌ | Frontier | $30 | $180 | 1.05M | ~2T (est) | San Francisco, US | US | ✅ |
| 2 | OpenAI | o3 Deep Research | ❌ | Frontier | — | $60 | 200K | ~2T (est) | San Francisco, US | US | ✅ |
| 3 | Anthropic | Claude Fable 5 | ❌ | Frontier | $10 | $50 | 1M | ~1T (est) | San Francisco, US | US | ✅ |
| 4 | Anthropic | Claude Sonnet 5 | ❌ | Strong | $2 | $10 | 1M | ~500B | San Francisco, US | US | ✅ |
| 5 | Google | Gemini 3.5 Flash | ❌ | Strong | $1.50 | $9 | 1M | — | Mountain View, US | US | ✅ |
| 6 | Google | Gemma 4 26B | ✅ | Mid | free | free | 262K | 26B | Mountain View, US | anywhere | ✅ |
| 7 | Meta | Llama 4 Maverick | ✅ | Strong | $0.18 | $0.40 | 164K | 400B MoE | Menlo Park, US | US / EU | ✅ |
| 8 | xAI | Grok Build 0.1 | ❌ | Strong | $1 | $2 | 256K | — | San Francisco, US | US | ✅ |
| 9 | Perplexity | Sonar Pro Search | ❌ | Specialist | $3 | $15 | 200K | — | San Francisco, US | US | ✅ |
| 10 | Writer | Palmyra X5 | ❌ | Strong | $0.60 | $6 | 1.04M | — | San Francisco, US | US | ✅ |
| 11 | Inflection | Inflection 3 | ❌ | Strong | $2.50 | $10 | 128K | — | Palo Alto, US | US | ✅ |
| 12 | Nvidia | Nemotron 3.5 4B | ✅ | Mid | free | free | 128K | 4B | Santa Clara, US | anywhere | ✅ |
| 13 | AI2 (Allen) | OLMo 3 32B Think | ✅ | Mid | $0.15 | $0.50 | 65K | 32B | Seattle, US | anywhere | ✅ |
| 14 | Microsoft | Phi-4 | ✅ | Mid | $0.07 | $0.14 | 16K | 14B | Redmond, US | anywhere | ✅ |
| 15 | IBM | Granite 4.1 8B | ✅ | Mid | $0.05 | $0.10 | 131K | 8B | US | anywhere | ✅ |
| 16 | Liquid | LFM 2.5 1.2B | ✅ | Mid | free | free | 33K | 1.2B | NYC / Zürich | anywhere | ✅ |
| 17 | Nous Research | Hermes 4 405B | ✅ | Strong | $1 | $3 | 131K | 405B | Remote / US | anywhere | ✅ |
| 18 | Mistral AI | Mistral Large 2512 | ❌ | Strong | $0.50 | $1.50 | 262K | 123B | Paris, FR | EU / US | ✅ |
| 19 | Mistral AI | Mistral Small 3.1 24B | ✅ | Mid | free | free | 128K | 24B | Paris, FR | anywhere | ✅ |
| 20 | Poolside | Laguna XS.2 | ❌ | Strong | free | free | 128K | — | Paris / SF | EU / US | ✅ |
| 21 | DeepCogito | Cogito V2.1 671B | ❌ | Strong | $1.25 | $1.25 | 128K | 671B | Paris / US | EU / US | ✅ |
| 22 | Reka AI | Reka Edge | ✅ | Mid | $0.05 | $0.10 | 128K | — | London, UK | anywhere | ✅ |
| 23 | Aleph Alpha | Luminous | ❌ | Mid | — | — | — | — | Heidelberg, DE | DE | ❌ |
| 24 | LightOn | LightOn | ❌ | Mid | — | — | — | — | Paris, FR | FR | ❌ |
| 25 | DeepL | DeepL Translate | ❌ | Specialist | — | — | — | — | Cologne, DE | DE | ❌ |
| 26 | Stability AI | Stable Diffusion | ✅ | Specialist | — | — | — | — | London, UK | anywhere | ❌ |
| 27 | Black Forest Labs | Flux | ✅ | Specialist | — | — | — | — | Stuttgart / Berlin, DE | anywhere | ❌ |
| 28 | DeepSeek | DeepSeek V4 Pro | ✅ | Frontier | $0.44 | $0.87 | 1.05M | 671B MoE | Hangzhou, CN | **CN + US/EU** | ✅ |
| 29 | Qwen (Alibaba) | Qwen 3.5 Plus | ✅ | Frontier | $0.30 | $1.80 | 1M | — | Hangzhou, CN | **CN + US/EU** | ✅ |
| 30 | Z.AI | GLM 5.2 | ✅ | Frontier | $0.93 | $3 | 1.05M | — | Shanghai, CN | **CN + US/EU** | ✅ |
| 31 | Moonshot AI | Kimi K2.7 | ❌ | Frontier | $0.38 | $2.03 | 262K | — | Beijing, CN | CN | ✅ |
| 32 | MiniMax | MiniMax M2.5 | ❌ | Strong | $0.12 | $0.48 | 205K | — | Shanghai, CN | CN | ✅ |
| 33 | Tencent | Hunyuan 3 | ❌ | Strong | $0.06 | $0.21 | 262K | — | Shenzhen, CN | CN | ✅ |
| 34 | Baidu | ERNIE 4.5 VL | ❌ | Strong | $0.42 | $1.25 | 131K | 424B | Beijing, CN | CN | ✅ |
| 35 | ByteDance | Seed 1.6 Flash | ❌ | Mid | $0.08 | $0.30 | 262K | — | Beijing, CN | CN | ✅ |
| 36 | StepFun | Step 3.5 Flash | ❌ | Mid | $0.08 | $0.30 | 262K | — | Beijing, CN | CN | ✅ |
| 37 | Xiaomi | MiMo 2.5 Pro | ❌ | Strong | $0.30 | $0.87 | 128K | — | Beijing, CN | CN | ✅ |
| 38 | Cohere | Command A | ❌ | Strong | $2.50 | $10 | 256K | — | Toronto / SF | US | ✅ |
| 39 | AI21 | Jamba Large 1.7 | ❌ | Strong | $2 | $8 | 256K | — | Tel Aviv, IL | US / IL | ✅ |
| 40 | Sakana AI | Fugu Ultra | ❌ | Specialist | $5 | $30 | 1M | multi-agent | Tokyo, JP | JP | ✅ |
| 41 | Upstage | Solar Pro 3 | ✅ | Mid | $0.15 | $0.60 | 128K | — | Seongnam, KR | KR / US | ✅ |

## Kapabilität (Größe der Punkte)

| Tier | Bedeutung | Beispiele |
|------|-----------|-----------|
| **Frontier** | Flaggschiff-Reasoning, top-tier | GPT-5.4 Pro, Claude Fable 5, DeepSeek V4 Pro, Qwen 3.5, GLM 5.2, Kimi K2.7 |
| **Strong** | Leistungsstarke Arbeitspferde | Claude Sonnet 5, Llama 4, Mistral Large, Command A, Hunyuan 3, ERNIE, Hermes 4 |
| **Mid** | Klein / effizient / Edge | Gemma 4, Phi-4, Granite, Nemotron, OLMo, Solar Pro, Reka Edge |
| **Specialist** | Bild / Übersetzung / Suche / Agent | Flux, Stable Diffusion, DeepL, Sonar Pro, Fugu Ultra |

## Farbskala (Output $/M)

| Farbe | Kosten | Beispiele |
|-------|--------|----------|
| 🟢 Grün | free – < $1 | Hunyuan ($0.21), Llama 4 ($0.40), MiniMax ($0.48), DeepSeek ($0.87) |
| 🟡 Gelbgrün | $1 – $5 | Mistral Large ($1.50), Qwen ($1.80), Grok ($2), GLM 5.2 ($3), Hermes 4 ($3) |
| 🟠 Orange | $5 – $15 | Palmyra X5 ($6), Jamba ($8), Command A / Sonnet 5 ($10), Sonar Pro ($15) |
| 🔴 Rot | $15 – $50 | Fugu Ultra ($30), Claude Fable 5 ($50) |
| 🔴 Maroon | > $50 | o3 Deep Research ($60), **GPT-5.4 Pro ($180)** |
| ⚪ Grau | nicht Token-bepreist | Luminous, LightOn, DeepL, Stable Diffusion, Flux |

## Herkunft vs. Hosting — der Kernpunkt

Der geopolitische Kern liegt im Unterschied zwischen **wo ein Modell herkommt** und **wo man es laufen lassen kann**:

- **Offene Modelle** (● gefüllt) sind selbst hostbar. Ein offenes chinesisches Modell (DeepSeek, Qwen, GLM) läuft problemlos auf US-/EU-Infrastruktur — die Daten müssen die eigene Jurisdiktion nicht verlassen. Auf der Karte zeigt der gestrichelte Bogen genau diesen West-Hosting-Pfad.
- **Geschlossene Modelle** (◌ Ring) binden an die Serving-Region des Labors. Ein geschlossenes chinesisches Modell (Kimi, Hunyuan, ERNIE, Seed, StepFun, MiMo) bedeutet: die Anfragen gehen nach China. Kein Bogen.

## Legende

- **Punkt (●)** = Open Weights (frei verfügbar, selbst hostbar)
- **Ring (◌)** = Closed Weights (nur via API)
- **Größe** = Kapabilität (Frontier > Strong > Mid > Specialist)
- **Gestrichelter Bogen** = offenes Modell, das im Westen (US/EU) gehostet werden kann
- **✅ = auf OpenRouter verfügbar** · **❌ = nur direkt (Direct API)**

## Quellen

- OpenRouter API `/api/v1/models` (Juli 2026): 338 Modelle von 50+ Labs
- Herkunft = Lab-HQ; Hosting basierend auf bekannten Inference-Providern (Together, DeepInfra, Fireworks etc.)
- Open/Closed basierend auf Modell-Lizenz; Kapabilität = Modellklasse (Schätzung, keine Benchmark-Rangliste)

# 🎙️ Banco Central de Vozes Humanizadas (`gabrielmoura735/vozes`)

> **Repositório Central de Vozes Reais e de Alta Fidelidade** para integração instantânea em qualquer produto digital, aplicativo, audiolivro, oração ou curso.
> 
> 🌐 **Catálogo & Player Online:** [https://gabrielmoura735.github.io/vozes/](https://gabrielmoura735.github.io/vozes/)

---

## ✨ Diferenciais do Banco de Vozes

1. **Zero Síntese Robótica de Navegador**:
   - Não depende do sintetizador padrão e mecânico do Windows/navegador (`speechSynthesis`).
   - Todas as vozes possuem arquivos de áudio autênticos em formato `.mp3` de estúdio.
2. **Vozes Humanas de Locutores Profissionais**:
   - Amostras reais extraídas de estúdios acústicos do **Clube dos Locutores** (masculinas e femininas) nos estilos: comercial, institucional, suave, grave, jovem e devocional.
3. **Vozes Neurais de Estúdio (ElevenLabs & Neural Studio PT-BR)**:
   - Amostras de estúdio neural com respiração, modulação calma e entonação natural para orações, reflexões e devocionais.
4. **Pronto para Reutilizar em Qualquer Projeto**:
   - Um script utilitário copia ou gera áudios para qualquer pasta de qualquer repositório em 1 único comando.

---

## 📁 Estrutura do Repositório

```
vozes/
├── index.html                          # Player e Catálogo Interativo Online (GitHub Pages)
├── banco_vozes.json                    # Base de dados estruturada de todas as vozes catalogadas
├── README.md                           # Documentação e guia de integração
├── scripts/
│   ├── coletar_vozes.py                # Script extrator automático de novas vozes
│   ├── integrar_voz.py                 # Utilitário para exportar voz para outro projeto
│   └── gerar_audio_projeto.py          # Gerador universal de áudio a partir de texto
└── amostras/
    ├── masculinas/                     # MP3s de locutores e vozes masculinas
    └── femininas/                      # MP3s de locutoras e vozes femininas
```

---

## 🚀 Como Integrar Vozes em Outros Projetos

### Método 1: Exportar Amostra / Arquivo MP3 para seu Projeto
Para copiar a voz para dentro de qualquer outro projeto no seu computador:

```bash
# Listar todas as vozes disponíveis
python scripts/integrar_voz.py --listar

# Exportar a voz feminina de oração (Francisca) para a pasta de áudio do seu produto
python scripts/integrar_voz.py --voz studio_francisca_devocional --destino ../MeuProduto/audio/

# Exportar locutor profissional do Clube dos Locutores
python scripts/integrar_voz.py --voz clube_edu-correia --destino ../MeuProduto/audio/
```

### Método 2: Gerar Novo Áudio Falado a partir de um Texto
Para narrar um texto devocional ou mensagem usando a voz humana de estúdio:

```bash
python scripts/gerar_audio_projeto.py \
  --texto "Senhor, coloco em Tuas mãos este dia. Renova minhas forças e guia meus passos." \
  --voz francisca \
  --saida ../MeuProduto/audio/oracao_diaria.mp3
```

**Vozes disponíveis para síntese direta:**
- `francisca`: Feminina - Calma / Clamor / Devocional
- `antonio`: Masculina - Pastoral / Narração / Firme
- `thalita`: Feminina - Serena / Meditação / Suave
- `donato`: Masculina - Sabedoria / Reflexão / Profundo
- `manuela`: Feminina - Clara / Dinâmica / Institucional
- `nicolau`: Masculina - Jovem / Moderno / Motivacional

### Método 3: Usar Diretamente no seu HTML com CDN do GitHub
Você pode tocar qualquer voz diretamente no seu site usando o link do GitHub Pages:

```html
<!-- Exemplo de player nativo com voz humana real -->
<audio controls preload="metadata">
  <source src="https://gabrielmoura735.github.io/vozes/amostras/femininas/studio_francisca_devocional.mp3" type="audio/mpeg">
  Seu navegador não suporta áudio.
</audio>
```

---

## 🎙️ Amostras de Vozes Catalogadas

| Locutor / Voz | Gênero | Origem | Estilo Principal |
| :--- | :--- | :--- | :--- |
| **Francisca** | Feminino | Estúdio Devocional | Oração / Clamor / Calma |
| **Antônio** | Masculino | Estúdio Devocional | Pastoral / Narração Firme |
| **Thalita** | Feminino | Estúdio Devocional | Serena / Meditativa / Acolhedora |
| **Donato** | Masculino | Estúdio Devocional | Sabedoria / Maturidade |
| **Edu Correia** | Masculino | Clube dos Locutores | Comercial / Institucional |
| **Mônica Bittencourt** | Feminino | Clube dos Locutores | Suave / Comercial |
| **Fabiano Vieira** | Masculino | Clube dos Locutores | Impacto / Narração |
| **Kátia Marques** | Feminino | Clube dos Locutores | Expressiva / Locução |
| **Roger** | Masculino | ElevenLabs | Casual / Resonant |
| **Sarah** | Feminino | ElevenLabs | Mature / Confident |
| *(E dezenas de outros)* | ... | ... | ... |

---

## 🔒 Licença e Direitos
- Amostras do Clube dos Locutores são propriedades dos respectivos locutores profissionais do Brasil para fins de demonstração e contratação de trabalhos.
- As vozes neurais e de estúdio estão pré-configuradas para uso livre nos produtos digitais do ecossistema.

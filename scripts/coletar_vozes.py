import os
import re
import json
import urllib.request
import urllib.parse
import time
import asyncio
import edge_tts

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMOSTRAS_DIR = os.path.join(BASE_DIR, 'amostras')
MASC_DIR = os.path.join(AMOSTRAS_DIR, 'masculinas')
FEM_DIR = os.path.join(AMOSTRAS_DIR, 'femininas')
JSON_FILE = os.path.join(BASE_DIR, 'banco_vozes.json')

os.makedirs(MASC_DIR, exist_ok=True)
os.makedirs(FEM_DIR, exist_ok=True)

banco_vozes = []

def download_file(url, dest_path, timeout=15):
    try:
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
            print(f"  [OK Já existe] {os.path.basename(dest_path)}")
            return True
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest_path, 'wb') as f:
                    f.write(data)
                print(f"  [Baixado] {os.path.basename(dest_path)} ({len(data)} bytes)")
                return True
    except Exception as e:
        print(f"  [Aviso download] {url}: {e}")
    return False

# ==========================================
# 1. COLETAR CLUBE DOS LOCUTORES
# ==========================================
def coletar_clube_dos_locutores():
    print("\n--- 1. Coletando Clube dos Locutores ---")
    urls_genero = [
        ('masculino', 'https://clubedoslocutores.com.br/genero/masculino/', MASC_DIR),
        ('feminino', 'https://clubedoslocutores.com.br/genero/feminino/', FEM_DIR)
    ]
    
    for genero, cat_url, pasta_dest in urls_genero:
        print(f"\nConsultando categoria {genero.upper()}...")
        try:
            req = urllib.request.Request(cat_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            
            perfis = list(dict.fromkeys(re.findall(r'href="(https://clubedoslocutores\.com\.br/locutores/[^"/]+)/?"', html)))
            print(f"Encontrados {len(perfis)} perfis {genero}s.")
            
            for perfil_url in perfis:
                slug = perfil_url.rstrip('/').split('/')[-1]
                nome_formatado = slug.replace('-', ' ').title()
                
                try:
                    time.sleep(0.5)
                    req_p = urllib.request.Request(perfil_url, headers=HEADERS)
                    with urllib.request.urlopen(req_p, timeout=12) as p_resp:
                        p_html = p_resp.read().decode('utf-8', errors='ignore')
                    
                    # Extrair trackUrls do player
                    match_tracks = re.search(r'var\s+trackUrls\s*=\s*(\[.*?\]);', p_html, re.DOTALL)
                    if match_tracks:
                        tracks_raw = match_tracks.group(1)
                        # Decodificar JSON
                        try:
                            tracks = json.loads(tracks_raw)
                        except:
                            tracks = []
                            # Fallback regex para extrair URLs
                            raw_urls = re.findall(r'"url":"([^"]+)"', tracks_raw)
                            for u in raw_urls:
                                tracks.append({"name": "Demo", "url": u.replace('\\/', '/')})
                        
                        if tracks:
                            # Pegar primeira faixa como amostra principal
                            primeira_faixa = tracks[0]
                            audio_url = primeira_faixa.get('url', '').replace('\\/', '/')
                            if audio_url:
                                filename = f"clube_{genero}_{slug}.mp3"
                                local_path = os.path.join(pasta_dest, filename)
                                rel_path = f"amostras/{'masculinas' if genero=='masculino' else 'femininas'}/{filename}"
                                
                                # Tentar baixar
                                success = download_file(audio_url, local_path)
                                
                                # Extrair estilos ou tags do HTML
                                estilos = ["Humano Real", "Locutor Profissional"]
                                if "comercial" in p_html.lower(): estilos.append("Comercial")
                                if "institucional" in p_html.lower(): estilos.append("Institucional")
                                if "jovem" in p_html.lower(): estilos.append("Jovem")
                                if "suave" in p_html.lower(): estilos.append("Suave")
                                if "grave" in p_html.lower(): estilos.append("Grave")
                                if "devocional" in p_html.lower() or "padrao" in p_html.lower(): estilos.append("Padrão")
                                
                                banco_vozes.append({
                                    "id": f"clube_{slug}",
                                    "nome": nome_formatado,
                                    "genero": genero,
                                    "origem": "Clube dos Locutores",
                                    "estilo": list(set(estilos)),
                                    "descricao": f"Voz humana real de locutor(a) profissional do Brasil ({primeira_faixa.get('name', 'Demo Principal')}).",
                                    "arquivo_local": rel_path if success else "",
                                    "url_remota": audio_url,
                                    "idioma": "pt-BR",
                                    "perfil_link": perfil_url
                                })
                                print(f"  + Cadastrado: {nome_formatado} ({len(tracks)} faixas)")
                except Exception as e_p:
                    print(f"  Erro ao processar perfil {slug}: {e_p}")
        except Exception as e_c:
            print(f"Erro ao acessar {cat_url}: {e_c}")

# ==========================================
# 2. COLETAR ELEVENLABS PREMADE VOICES
# ==========================================
def coletar_elevenlabs():
    print("\n--- 2. Coletando Amostras ElevenLabs ---")
    url = 'https://api.elevenlabs.io/v1/voices'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            voices = data.get('voices', [])
            print(f"Encontradas {len(voices)} vozes na API ElevenLabs.")
            
            for v in voices:
                nome = v.get('name')
                labels = v.get('labels', {})
                genero = labels.get('gender', 'masculino').lower()
                if 'female' in genero:
                    genero = 'feminino'
                    pasta_dest = FEM_DIR
                    rel_dir = 'femininas'
                else:
                    genero = 'masculino'
                    pasta_dest = MASC_DIR
                    rel_dir = 'masculinas'
                
                preview_url = v.get('preview_url')
                slug = re.sub(r'[^a-zA-Z0-9]', '_', nome.lower()).strip('_')
                filename = f"eleven_{slug}.mp3"
                local_path = os.path.join(pasta_dest, filename)
                rel_path = f"amostras/{rel_dir}/{filename}"
                
                success = False
                if preview_url:
                    success = download_file(preview_url, local_path)
                
                estilos = ["Neural Studio", "ElevenLabs"]
                if labels.get('accent'): estilos.append(labels.get('accent').title())
                if labels.get('description'): estilos.append(labels.get('description').title())
                if labels.get('use case'): estilos.append(labels.get('use case').title())
                
                banco_vozes.append({
                    "id": f"eleven_{slug}",
                    "nome": f"{nome} (ElevenLabs)",
                    "genero": genero,
                    "origem": "ElevenLabs",
                    "estilo": estilos,
                    "descricao": v.get('description') or f"Voz neural de estúdio ElevenLabs ({labels.get('accent', 'English')}).",
                    "arquivo_local": rel_path if success else "",
                    "url_remota": preview_url or "",
                    "idioma": "en-US",
                    "perfil_link": "https://elevenlabs.io/app/voice-library"
                })
                print(f"  + Cadastrado ElevenLabs: {nome} ({genero})")
    except Exception as e:
        print(f"Erro ao coletar ElevenLabs: {e}")

# ==========================================
# 3. GERAR AMOSTRAS ESTÚDIO NEURAL PT-BR
# ==========================================
async def gerar_amostras_neurais_pt():
    print("\n--- 3. Gerando Amostras Neurais Brasileiras de Estúdio ---")
    vozes_pt = [
        {
            "id": "studio_francisca_devocional",
            "nome": "Francisca (Clamor & Oração)",
            "genero": "feminino",
            "voice": "pt-BR-FranciscaNeural",
            "rate": "-4%",
            "pitch": "+0Hz",
            "texto": "Pai Celestial, neste novo dia eu entrego meus passos em Tuas mãos. Que a Tua paz repouse sobre o meu coração e que Tua sabedoria me guie em cada decisão.",
            "estilo": ["Devocional", "Calma", "Oração", "Acolhedora", "Humana"],
            "descricao": "Voz feminina devocional suave com pausas acolhedoras para momentos de reflexão e oração matinal."
        },
        {
            "id": "studio_antonio_narrador",
            "nome": "Antônio (Narração Pastoral)",
            "genero": "masculino",
            "voice": "pt-BR-AntonioNeural",
            "rate": "-3%",
            "pitch": "-1Hz",
            "texto": "O Senhor é o meu pastor, e nada me faltará. Ainda que eu ande pelo vale da sombra da morte, não temerei mal algum, porque Tu estás comigo.",
            "estilo": ["Pastoral", "Narrador", "Grave", "Firme", "Inspirador"],
            "descricao": "Voz masculina pastoral firme, ideal para audiolivros, devocionais e mensagens edificantes de autoridade."
        },
        {
            "id": "studio_thalita_acolhedora",
            "nome": "Thalita (Serena & Inspiradora)",
            "genero": "feminino",
            "voice": "pt-BR-ThalitaNeural",
            "rate": "-2%",
            "pitch": "+0Hz",
            "texto": "Aquietai-vos e sabei que Eu sou Deus. Respire fundo, solte todas as preocupações e sinta a renovação espiritual fluir em sua vida hoje.",
            "estilo": ["Suave", "Serena", "Meditativa", "Jovem"],
            "descricao": "Voz feminina meditativa serena, perfeita para reprogramação mental, relaxamento e meditações guiadas."
        },
        {
            "id": "studio_donato_inspirador",
            "nome": "Donato (Sabedoria & Calmaria)",
            "genero": "masculino",
            "voice": "pt-BR-DonatoNeural",
            "rate": "-4%",
            "pitch": "-2Hz",
            "texto": "A sabedoria edifica a casa e pelo entendimento ela se estabelece. Cada desafio que surge é uma oportunidade de crescimento com propósito.",
            "estilo": ["Maduro", "Sabedoria", "Calmo", "Profundo"],
            "descricao": "Voz masculina madura e reconfortante, com tom de mestre e mentor para guias de estudo."
        },
        {
            "id": "studio_manuela_expressiva",
            "nome": "Manuela (Clara & Dinâmica)",
            "genero": "feminino",
            "voice": "pt-BR-ManuelaNeural",
            "rate": "+0%",
            "pitch": "+0Hz",
            "texto": "Bem-vindo ao seu portal diário. Aqui você encontra as ferramentas, áudios e orientações necessárias para alcançar uma rotina abençoada.",
            "estilo": ["Dinâmica", "Clara", "Educacional", "Institucional"],
            "descricao": "Voz feminina clara e engajadora, ideal para tutoriais, boas-vindas e introdução de módulos."
        },
        {
            "id": "studio_nicolau_moderno",
            "nome": "Nicolau (Jovem & Atual)",
            "genero": "masculino",
            "voice": "pt-BR-NicolauNeural",
            "rate": "+0%",
            "pitch": "+0Hz",
            "texto": "A constância é a chave para a transformação duradoura. Mantenha o foco em seus objetivos e celebre cada pequena vitória de hoje.",
            "estilo": ["Jovem", "Comercial", "Moderno", "Motivacional"],
            "descricao": "Voz masculina contemporânea e motivacional para conteúdos práticos e podcasts dinâmicos."
        }
    ]
    
    for v in vozes_pt:
        genero = v['genero']
        pasta = FEM_DIR if genero == 'feminino' else MASC_DIR
        rel_dir = 'femininas' if genero == 'feminino' else 'masculinas'
        filename = f"{v['id']}.mp3"
        dest_path = os.path.join(pasta, filename)
        rel_path = f"amostras/{rel_dir}/{filename}"
        
        try:
            communicate = edge_tts.Communicate(v['texto'], v['voice'], rate=v['rate'], pitch=v['pitch'])
            await communicate.save(dest_path)
            print(f"  [Gerado Studio] {filename} ({os.path.getsize(dest_path)} bytes)")
            
            banco_vozes.append({
                "id": v['id'],
                "nome": v['nome'],
                "genero": v['genero'],
                "origem": "Estúdio Devocional Neural",
                "estilo": v['estilo'],
                "descricao": v['descricao'],
                "arquivo_local": rel_path,
                "url_remota": "",
                "idioma": "pt-BR",
                "perfil_link": "https://github.com/gabrielmoura735/vozes"
            })
        except Exception as e:
            print(f"  Erro ao gerar {v['id']}: {e}")

# ==========================================
# MAIN EXECUTION
# ==========================================
def main():
    print("Iniciando coleta completa para o repositório 'vozes'...")
    
    # 1. Clube dos Locutores
    coletar_clube_dos_locutores()
    
    # 2. ElevenLabs
    coletar_elevenlabs()
    
    # 3. Estúdio Neural PT-BR
    asyncio.run(gerar_amostras_neurais_pt())
    
    # Salvar banco de dados JSON
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(banco_vozes, f, indent=2, ensure_ascii=False)
    
    # Salvar cópia em data/
    with open(os.path.join(BASE_DIR, 'data', 'banco_vozes.json'), 'w', encoding='utf-8') as f:
        json.dump(banco_vozes, f, indent=2, ensure_ascii=False)
        
    print(f"\n==========================================")
    print(f"TOTAL DE VOZES CATALOGADAS: {len(banco_vozes)}")
    masc_count = len([v for v in banco_vozes if v['genero'] == 'masculino'])
    fem_count = len([v for v in banco_vozes if v['genero'] == 'feminino'])
    print(f"Masculinas: {masc_count}")
    print(f"Femininas: {fem_count}")
    print(f"Banco salvo em: {JSON_FILE}")
    print(f"==========================================")

if __name__ == '__main__':
    main()

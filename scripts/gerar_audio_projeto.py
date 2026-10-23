"""
Gerador de Áudio Neural com Vozes Humanizadas (gabrielmoura735/vozes)
Permite sintetizar qualquer texto em MP3 com qualidade de estúdio e entonação natural.

Exemplo de uso:
  python scripts/gerar_audio_projeto.py --texto "Senhor, ilumina meus passos neste dia." --voz francisca --saida ./oracao_hoje.mp3
"""

import os
import sys
import asyncio
import argparse
import edge_tts

MAPA_VOZES = {
    "francisca": {
        "voice": "pt-BR-FranciscaNeural",
        "rate": "-4%",
        "pitch": "+0Hz",
        "desc": "Feminina - Calma / Clamor / Devocional"
    },
    "antonio": {
        "voice": "pt-BR-AntonioNeural",
        "rate": "-3%",
        "pitch": "-1Hz",
        "desc": "Masculina - Pastoral / Narração / Firme"
    },
    "thalita": {
        "voice": "pt-BR-ThalitaNeural",
        "rate": "-2%",
        "pitch": "+0Hz",
        "desc": "Feminina - Serena / Meditação / Suave"
    },
    "donato": {
        "voice": "pt-BR-DonatoNeural",
        "rate": "-4%",
        "pitch": "-2Hz",
        "desc": "Masculina - Maduro / Sabedoria / Profundo"
    },
    "manuela": {
        "voice": "pt-BR-ManuelaNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Feminina - Clara / Dinâmica / Institucional"
    },
    "nicolau": {
        "voice": "pt-BR-NicolauNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "desc": "Masculina - Jovem / Moderno / Motivacional"
    }
}

async def sintetizar(texto, voz_key, caminho_saida):
    config = MAPA_VOZES.get(voz_key.lower())
    if not config:
        print(f"Erro: Voz '{voz_key}' não reconhecida. Opções: {', '.join(MAPA_VOZES.keys())}")
        return False
    
    os.makedirs(os.path.dirname(os.path.abspath(caminho_saida)), exist_ok=True)
    print(f"Gerando áudio com a voz: {voz_key.upper()} ({config['desc']})...")
    
    communicate = edge_tts.Communicate(texto, config['voice'], rate=config['rate'], pitch=config['pitch'])
    await communicate.save(caminho_saida)
    
    if os.path.exists(caminho_saida) and os.path.getsize(caminho_saida) > 0:
        print(f"[SUCESSO] Áudio gerado: {caminho_saida} ({os.path.getsize(caminho_saida)} bytes)")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Gerador de Áudio Neural Humanizado")
    parser.add_argument('--texto', type=str, required=True, help='Texto a ser narrado')
    parser.add_argument('--voz', type=str, default='francisca', choices=list(MAPA_VOZES.keys()), help='Voz escolhida')
    parser.add_argument('--saida', type=str, default='audio_gerado.mp3', help='Caminho do arquivo MP3 de saída')
    
    args = parser.parse_args()
    asyncio.run(sintetizar(args.texto, args.voz, args.saida))

if __name__ == '__main__':
    main()

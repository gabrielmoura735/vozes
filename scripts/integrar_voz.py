"""
Utilitário de Integração do Banco de Vozes (gabrielmoura735/vozes)
Permite exportar qualquer voz ou amostra diretamente para qualquer projeto.

Exemplos de uso:
  python scripts/integrar_voz.py --listar
  python scripts/integrar_voz.py --voz studio_francisca_devocional --destino ../NovoProjeto/audio/
  python scripts/integrar_voz.py --voz clube_edu-correia --destino ../OutroProjeto/
"""

import os
import sys
import json
import shutil
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE = os.path.join(BASE_DIR, 'banco_vozes.json')

def carregar_banco():
    if not os.path.exists(JSON_FILE):
        print(f"Erro: Banco de vozes não encontrado em {JSON_FILE}")
        sys.exit(1)
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def listar_vozes(filtro_genero=None):
    vozes = carregar_banco()
    print("\n=======================================================")
    print(f"BANCO DE VOZES DISPONÍVEIS ({len(vozes)} vozes)")
    print("=======================================================\n")
    for v in vozes:
        if filtro_genero and v['genero'].lower() != filtro_genero.lower():
            continue
        estilos = ", ".join(v.get('estilo', []))
        local = "[Áudio Local OK]" if v.get('arquivo_local') else "[Apenas Remoto]"
        print(f"ID: {v['id']}")
        print(f"  Nome: {v['nome']} | Gênero: {v['genero'].title()} | Origem: {v['origem']}")
        print(f"  Estilos: {estilos}")
        print(f"  Status: {local}")
        print(f"  URL Direta: {v.get('url_remota') or 'N/A'}")
        print("-" * 55)

def exportar_voz(voz_id, destino):
    vozes = carregar_banco()
    voz = next((v for v in vozes if v['id'] == voz_id or voz_id.lower() in v['nome'].lower()), None)
    if not voz:
        print(f"Erro: Voz '{voz_id}' não encontrada no banco.")
        return False
    
    os.makedirs(destino, exist_ok=True)
    
    if voz.get('arquivo_local'):
        origem_path = os.path.join(BASE_DIR, voz['arquivo_local'])
        if os.path.exists(origem_path):
            nome_arq = os.path.basename(origem_path)
            dest_file = os.path.join(destino, nome_arq)
            shutil.copy2(origem_path, dest_file)
            print(f"\n[SUCESSO] Voz '{voz['nome']}' copiada para:")
            print(f"  -> {dest_file}")
            print(f"\nSnippet para usar no seu HTML:")
            print(f'<audio controls src="{nome_arq}"></audio>')
            return True
    
    if voz.get('url_remota'):
        print(f"\n[URL REMOTA] Voz '{voz['nome']}' disponível em:")
        print(f"  -> {voz['url_remota']}")
        print(f"\nSnippet para usar no seu HTML:")
        print(f'<audio controls src="{voz["url_remota"]}"></audio>')
        return True
        
    print(f"Aviso: Não foi possível localizar arquivo físico ou URL para {voz_id}")
    return False

def main():
    parser = argparse.ArgumentParser(description="Integrador do Banco de Vozes")
    parser.add_argument('--listar', action='store_true', help='Listar todas as vozes catalogadas')
    parser.add_argument('--genero', choices=['masculino', 'feminino'], help='Filtrar por gênero')
    parser.add_argument('--voz', type=str, help='ID ou nome da voz para integrar')
    parser.add_argument('--destino', type=str, default='.', help='Pasta de destino no seu produto')
    
    args = parser.parse_args()
    
    if args.listar or len(sys.argv) == 1:
        listar_vozes(args.genero)
    elif args.voz:
        exportar_voz(args.voz, args.destino)

if __name__ == '__main__':
    main()

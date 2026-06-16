#!/usr/bin/env python3
import sys
import requests

def main():
    # URL запрашивает только запущенные реле и только нужные поля (or_addresses и fingerprint)
    url = "https://onionoo.torproject.org/details?type=relay&running=true&fields=fingerprint,or_addresses"
    output_file = "vanilla_bridges.txt"

    print("Получение списка реле из Onionoo...", file=sys.stderr)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}", file=sys.stderr)
        sys.exit(1)

    relays = data.get("relays", [])
    print(f"Найдено реле: {len(relays)}. Запись в {output_file}...", file=sys.stderr)

    lines_written = 0
    with open(output_file, "w") as f:
        for relay in relays:
            fingerprint = relay.get("fingerprint")
            or_addresses = relay.get("or_addresses", [])
            
            if fingerprint:
                for addr in or_addresses:
                    # Записывает в формате: IP:PORT FINGERPRINT
                    f.write(f"{addr} {fingerprint}\n")
                    lines_written += 1

    print(f"Готово! В файл записано {lines_written} строк мостов.", file=sys.stderr)

if __name__ == "__main__":
    main()

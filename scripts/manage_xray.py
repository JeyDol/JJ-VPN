import json
import sys
import subprocess
from pathlib import Path

XRAY_CONFIG_PATH = Path("/usr/local/etc/xray/config.json")


def load_config():
    with open(XRAY_CONFIG_PATH, 'r') as f:
        return json.load(f)


def save_config(config):
    with open(XRAY_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def restart_xray():
    subprocess.run(["systemctl", "restart", "xray"], check=True)


def add_user(uuid: str, email: str = None):
    config = load_config()

    for inbound in config.get("inbounds", []):
        if inbound.get("protocol") == "vless":
            clients = inbound.get("settings", {}).get("clients", [])


            if any(c.get("id") == uuid for c in clients):
                print(f" UUID {uuid} уже существует!")
                return False

            new_client = {
                "id": uuid,
                "flow": "xtls-rprx-vision",
                "email": email or f"user-{uuid[:8]}"
            }
            clients.append(new_client)


            save_config(config)
            restart_xray()

            print(f"Пользователь {uuid} добавлен!")
            return True

    print(" VLESS inbound не найден в конфиге!")
    return False


def remove_user(uuid: str):
    config = load_config()

    for inbound in config.get("inbounds", []):
        if inbound.get("protocol") == "vless":
            clients = inbound.get("settings", {}).get("clients", [])


            original_count = len(clients)
            clients[:] = [c for c in clients if c.get("id") != uuid]

            if len(clients) < original_count:
                save_config(config)
                restart_xray()
                print(f"Пользователь {uuid} удалён!")
                return True
            else:
                print(f"UUID {uuid} не найден!")
                return False

    print("VLESS inbound не найден!")
    return False


def list_users():
    config = load_config()

    for inbound in config.get("inbounds", []):
        if inbound.get("protocol") == "vless":
            clients = inbound.get("settings", {}).get("clients", [])

            print(f"Пользователи Xray ({len(clients)}):\n")
            for i, client in enumerate(clients, 1):
                print(f"{i}. UUID: {client.get('id')}")
                print(f"   Email: {client.get('email', 'N/A')}")
                print(f"   Flow: {client.get('flow', 'N/A')}\n")

            return

    print("VLESS inbound не найден!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage_xray.py add <uuid> [email]")
        print("  python manage_xray.py remove <uuid>")
        print("  python manage_xray.py list")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Укажите UUID!")
            sys.exit(1)
        uuid = sys.argv[2]
        email = sys.argv[3] if len(sys.argv) > 3 else None
        add_user(uuid, email)

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Укажите UUID!")
            sys.exit(1)
        uuid = sys.argv[2]
        remove_user(uuid)

    elif command == "list":
        list_users()

    else:
        print(f"Неизвестная команда: {command}")
        sys.exit(1)
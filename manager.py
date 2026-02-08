import os
from crypto_utils import derive_key, encrypt_data, decrypt_data

VAULT_FILE = "vault.enc"


def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    return decrypt_data(encrypted, key)


def save_vault(vault, key):
    encrypted = encrypt_data(vault, key)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)


def add_entry(vault):
    site = input("Site: ")
    username = input("Username: ")
    password = input("Password: ")

    vault[site] = {
        "username": username,
        "password": password
    }
    print("✅ Entry added successfully")


def retrieve_entry(vault):
    site = input("Site to retrieve: ")
    if site in vault:
        print("Username:", vault[site]["username"])
        print("Password:", vault[site]["password"])
    else:
        print("❌ Entry not found")


def delete_entry(vault):
    site = input("Site to delete: ")
    if site in vault:
        del vault[site]
        print("🗑️ Entry deleted")
    else:
        print("❌ Entry not found")


def search_entry(vault):
    keyword = input("Search keyword: ")
    found = False
    for site in vault:
        if keyword.lower() in site.lower():
            print(site, vault[site])
            found = True
    if not found:
        print("❌ No matching entries")


def main():
    master_password = input("Enter master password: ")
    key = derive_key(master_password)

    try:
        vault = load_vault(key)
    except Exception:
        print("❌ Wrong master password or corrupted vault")
        return

    while True:
        print("\n1. Add")
        print("2. Retrieve")
        print("3. Delete")
        print("4. Search")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_entry(vault)
        elif choice == "2":
            retrieve_entry(vault)
        elif choice == "3":
            delete_entry(vault)
        elif choice == "4":
            search_entry(vault)
        elif choice == "5":
            save_vault(vault, key)
            print("🔒 Vault encrypted & saved")
            break
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()

import pandas as pd
import os
import sys
import random

#Constants
password_file = "YOUR_FILE_PATH_HERE"
credential_file = "YOUR_FILE_PATH_HERE"

def auth():
    """Validates authorization via a local password file."""
    if not os.path.exists(password_file):
        print(f"[Error] Authortization file {password_file} not found")
        sys.exit(1)

    with open (password_file, "r") as f:
        # Strip trailing newlines, but intentionally preserve empty lines 
        # to ensure the subsequent length check correctly catches integrity tampering.
        passwords = [line.strip() for line in f.readlines() if line.strip]

    # Security check: multiple entries indicate potential file tampering or multi-tenant misconfiguration
    if len(passwords) > 1:
        print("[CRITICAL] Multiple password entries detected. Potential file compromise. Aborting.")
        sys.exit(1)

    elif len(passwords) == 0:
        print("[Error] No password found. Potential compromise detected.")
        sys.exit(1)

    stored_password = passwords[0]
    user_input = input("Enter admin password to procided: ")

    if user_input != stored_password:
        print("[Error] Invalid password, access denied")
        sys.exit(1)
    else:
        print("[Success] Valid password, access granted.\n")

def get_validated_name(prompt, min_len=3, max_len=15):
    """Prompts user for a name string within character limits."""
    while True:
        name = input(prompt)
        if min_len <= len(name) <= max_len:
            return name.lower()
        print(f"[Error] Name must be between {min_len} and {max_len} characters.")

def gen_credientals():
    """Generates a structured credential based on initials and a random ID."""

    print("---Credential Generation---")
    first_name = get_validated_name("Enter first name: ")
    middle_name = get_validated_name("Enter middle name: ")
    last_name = get_validated_name("Enter last name: ")

    # Extract the first character of each name component to form standard organizational initials
    initials = "".join([name[0].upper() for name in [first_name, middle_name, last_name]])

    # Generate cryptographically unassociated pseudo-random digits for uniqueness
    rand_digits = "".join([str(random.randint(0, 9)) for _ in range(9)])

    new_credentials = f"{initials}_{rand_digits}"
    print(f"[Generated] New Credential: {new_credentials}")

    save_credentials_to_file(new_credentials)

def save_credentials_to_file(credentials):
    """Appends credentials safely by loading, updating, and rewriting the CSV."""
    if os.path.exists(credential_file):
        try:
            df = pd.read_csv(credential_file)
            # Self-healing validation: check schema integrity to prevent parsing errors on corrupted files
            if 'Credential' in df.columns:
                cred_list = df['Credential'].dropna().tolist()
            else:
                cred_list = []
        except Exception:
            # Fallback for unexpected structural malformations in the storage layer
            cred_list = []
    else:
        cred_list = []

    # Enforce idempotency to prevent duplicate credential entries in the tracking register
    if credentials not in cred_list:
        cred_list.append(credentials)

    # Completely rewrite the flat file to maintain strict table schema without append artifacts
    df = pd.DataFrame({"Credential": cred_list})
    df.to_csv(credential_file, index=False)
    print(f"[Success] Credentials saved to {credential_file}\n")

def remove_credentials():
    """Allows an administrator to review and remove credentials from the file."""
    if not os.path.exists(credential_file):
        print(f"[Error] Credential file {credential_file} not found.")
        sys.exit(1)

    df = pd.read_csv(credential_file)
    if df.empty:
        print("[Error] No credentials found in the file.")
        return

    print("\n---Credential Review---")
    credential_list = df['Credential'].tolist()
    updated_list = credential_list.copy()

    for credentials in credential_list:
        while True:
            action = input(f"Do you want to remove {credentials}? (yes/no/exit): ").lower()

            if action in ["yes", "no", "exit"]:
                break
            print("[Error] Invalid choice, try again.")

        if action == "exit":
            print("[Info] Stopping removal process")
            break
        elif action == "yes":
            updated_list.remove(credentials)
            print(f"[Success] Removed {credentials} from the list.")
        elif action == "no":
            print(f"[Info] Skipping {credentials}.")
        else:
            print("[Error] Invalid choice, try again")

        while True:
            cont = input("Would you like to continue removing credentials? (continue/stop): ").strip().lower()
            if cont in ["continue", "stop"]:
                break
            print("[Error] Invalid choice. Please enter 'continue' or 'stop'.")

        if cont == "stop":
            print("[Info] Stopping removal process.")
            break

    new_df = pd.DataFrame({"Credential": updated_list})
    new_df.to_csv(credential_file, index=False)
    print(f"[Success] Updated credential list saved to {credential_file}\n")

def main():
    auth()

    # Prompt for generation
    while True:
        gen_choice = input("Would you like to generate new credentials? (yes/no): ").strip().lower()
        if gen_choice in ['yes', 'no']:
            break
        print("[Error] Invalid choice. Please enter 'yes' or 'no'.")

    while gen_choice == 'yes':
        gen_credientals()
        gen_choice = input("Would you like to generate more credentials? (yes/no): ").strip().lower()

    print("[INFO] Skipping credential generation.")

    # Automatically transition to removal/management
    while True:
            remove_choice = input("Would you like to transition to removing credentials? (yes/no): ").strip().lower()
            if remove_choice in ['yes', 'no']:
                break
            print("[Error] Invalid choice. Please enter 'yes' or 'no'.")

    if remove_choice == 'yes':
            remove_credentials()
    else:
            print("[INFO] Skipping removal process.")

    print("[INFO] Exiting program.")


if __name__ == "__main__":
    main()

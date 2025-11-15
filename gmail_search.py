#!/usr/bin/env python3
"""
Gmail epasta adrešu meklēšanas rīks.
Meklē epasta adreses Gmail kontā (TO laukā) un ģenerē pārskatu.
"""

import os
import re
import csv
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope - tikai lasīšana
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """
    Autentificējas Gmail API izmantojot OAuth 2.0.

    Returns:
        Gmail API service objekts
    """
    creds = None

    # Token fails glabā lietotāja piekļuves un refresh token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Ja nav derīgu credentials, ļaujam lietotājam pieteikties
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ KĻŪDA: Nav atrasts credentials.json fails!")
                print("   Lūdzu sekojiet instrukcijām README.md failā.")
                exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Saglabājam credentials nākamajam palaišanas reizei
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def load_email_addresses(filename='nosutiti.txt'):
    """
    Nolasa epasta adreses no faila.

    Args:
        filename: Faila nosaukums ar epasta adresēm

    Returns:
        List ar epasta adresēm
    """
    emails = []

    if not os.path.exists(filename):
        print(f"❌ KĻŪDA: Fails {filename} nav atrasts!")
        exit(1)

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

        # Meklējam epasta adreses ar regex
        # Atbalsta formātus: "email@example.com", email@example.com
        email_pattern = r'["\']?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})["\']?'
        found_emails = re.findall(email_pattern, content)

        for email in found_emails:
            email = email.strip().lower()
            if email and email not in emails:
                emails.append(email)

    print(f"📧 Ielādētas {len(emails)} unikālas epasta adreses")
    return emails


def search_email_in_gmail(service, email_address):
    """
    Meklē konkrētu epasta adresi Gmail TO laukā.

    Args:
        service: Gmail API service objekts
        email_address: Epasta adrese, ko meklēt

    Returns:
        int: Atrasto ziņojumu skaits
    """
    try:
        # Gmail meklēšanas query - meklējam TO laukā
        query = f'to:{email_address}'

        # Meklējam ziņojumus
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=1  # Mums pietiek zināt, vai ir vismaz viens rezultāts
        ).execute()

        messages = results.get('messages', [])

        # Ja vajag precīzu skaitu, var iegūt resultSizeEstimate
        if messages:
            # Iegūstam kopējo skaitu
            total_results = results.get('resultSizeEstimate', len(messages))
            return total_results

        return 0

    except HttpError as error:
        print(f"   ⚠️  Kļūda meklējot {email_address}: {error}")
        return -1  # -1 nozīmē kļūdu


def generate_report(results, output_file='rezultats.csv'):
    """
    Ģenerē CSV pārskatu ar rezultātiem.

    Args:
        results: Dict ar rezultātiem {email: count}
        output_file: Izvades faila nosaukums
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Sadalām atrastos un neatrastos
    found = {email: count for email, count in results.items() if count > 0}
    not_found = {email: count for email, count in results.items() if count == 0}
    errors = {email: count for email, count in results.items() if count < 0}

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(['Gmail Epasta Adrešu Meklēšanas Rezultāti'])
        writer.writerow(['Ģenerēts:', timestamp])
        writer.writerow([])

        # Kopsavilkums
        writer.writerow(['KOPSAVILKUMS'])
        writer.writerow(['Kopā pārbaudītas adreses:', len(results)])
        writer.writerow(['Atrastas:', len(found)])
        writer.writerow(['Nav atrastas:', len(not_found)])
        if errors:
            writer.writerow(['Kļūdas:', len(errors)])
        writer.writerow([])

        # Neatrastas adreses (galvenais, ko lietotājs vēlas)
        writer.writerow(['NEATRASTAS EPASTA ADRESES (TO laukā)'])
        writer.writerow(['Epasta adrese'])
        for email in sorted(not_found.keys()):
            writer.writerow([email])
        writer.writerow([])

        # Atrastas adreses
        writer.writerow(['ATRASTAS EPASTA ADRESES'])
        writer.writerow(['Epasta adrese', 'Ziņojumu skaits'])
        for email, count in sorted(found.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([email, count])

        # Kļūdas, ja tādas bija
        if errors:
            writer.writerow([])
            writer.writerow(['KĻŪDAS MEKLĒJOT'])
            writer.writerow(['Epasta adrese'])
            for email in sorted(errors.keys()):
                writer.writerow([email])

    print(f"\n✅ Pārskats saglabāts: {output_file}")
    print(f"\n📊 KOPSAVILKUMS:")
    print(f"   Kopā pārbaudītas: {len(results)}")
    print(f"   ✓ Atrastas: {len(found)}")
    print(f"   ✗ Nav atrastas: {len(not_found)}")
    if errors:
        print(f"   ⚠ Kļūdas: {len(errors)}")


def main():
    """Galvenā funkcija."""
    print("=" * 60)
    print("Gmail Epasta Adrešu Meklēšanas Rīks")
    print("=" * 60)
    print()

    # 1. Ielādējam epasta adreses
    emails = load_email_addresses('nosutiti.txt')

    if not emails:
        print("❌ Nav atrasta neviena epasta adrese!")
        exit(1)

    # 2. Autentificējamies Gmail API
    print("\n🔐 Autentificēšanās Gmail API...")
    service = authenticate_gmail()
    print("✅ Autentifikācija veiksmīga!")

    # 3. Meklējam katru adresi
    print(f"\n🔍 Meklēju {len(emails)} adreses Gmail kontā (TO laukā)...")
    print("    (Tas var aizņemt dažas minūtes...)\n")

    results = {}

    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] Meklēju: {email}...", end=' ')
        count = search_email_in_gmail(service, email)
        results[email] = count

        if count > 0:
            print(f"✓ Atrasti {count} ziņojumi")
        elif count == 0:
            print("✗ Nav atrasts")
        else:
            print("⚠ Kļūda")

    # 4. Ģenerējam pārskatu
    print("\n📝 Ģenerēju pārskatu...")
    generate_report(results)

    print("\n✅ Gatavs!")
    print("=" * 60)


if __name__ == '__main__':
    main()

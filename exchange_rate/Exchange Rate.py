import requests

API_KEY = "YOUR_API_KEY"

base = input("Enter base currency (e.g., USD): ").upper()
target = input("Enter target currency (e.g., KES): ").upper()
amount = float(input("Enter amount: "))

url = f"https://v6.exchangerate-api.com/v6/ac60f1e030747f714e5d826f/latest/USD"
response = requests.get(url)
data = response.json()

if response.status_code != 200 or target not in data["conversion_rates"]:
    print("Error: Invalid currency code or API limit reached.")
else:
    rate = data["conversion_rates"][target]
    converted = amount * rate
    print(f"{amount} {base} = {converted:.2f} {target}")

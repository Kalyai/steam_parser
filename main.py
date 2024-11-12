from parser_patterns import parsing

def main():
    urls_desert_eagle_heat_treated = [
    "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Battle-Scarred%29",
    "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Well-Worn%29",
    "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Field-Tested%29",
    "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Minimal%20Wear%29",
    "https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Heat%20Treated%20%28Factory%20New%29"
    ]

    for url in urls_desert_eagle_heat_treated:
        print(f"Начала парситься: {url}")
        parsing(url)

if __name__ == "__main__":
    main()
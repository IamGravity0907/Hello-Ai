import time, pandas as pd, random
from textblob import TextBlob
from colorama import init, Fore
init(autoreset=True)

# Dummy data
data = {
    'Series_Title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
    'Genre': ['Action, Thriller', 'Drama', 'Comedy, Romance', 'Action', 'Drama, Thriller'],
    'IMDB_Rating': [8.5, 7.8, 8.0, 8.2, 7.9],
    'Overview': [
        'Exciting action movie',
        'A sad drama',
        'Funny and romantic',
        'Lots of action',
        'Thriller with twists'
    ]
}
df = pd.DataFrame(data)

genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})

def dots():
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.5)

def senti(p):
    return "Positive 😊" if p > 0 else "Negative 😞" if p < 0 else "Neutral 😐"

def recommend(genre=None, mood=None, rating=None, n=1):
    d = df
    if genre:
        d = d[d["Genre"].str.contains(genre, case=False, na=False)]
    if rating is not None:
        d = d[d["IMDB_Rating"] >= rating]
    if d.empty:
        return "No suitable movie recommendations found."
    d, need_nonneg, out = d.sample(frac=1).reset_index(drop=True), bool(mood), []
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov):
            continue
        pol = TextBlob(ov).sentiment.polarity
        if (not need_nonneg) or pol >= 0:
            out.append((r["Series_Title"], r["Genre"], ov, r["IMDB_Rating"], pol))
        if len(out) == n:
            break
    return out if out else "No suitable movie recommendations found."

def show(rec):
    t, g, o, r, p = rec
    print(Fore.YELLOW + f"\n🎥 {t}")
    print(Fore.CYAN + f"Genre: {g}")
    print(Fore.CYAN + f"Overview: {o}")
    print(Fore.CYAN + f"IMDB Rating: {r}")
    print(Fore.CYAN + f"Sentiment: {senti(p)}")

def get_genre():
    print(Fore.GREEN + "Available Genres: ", end="")
    for i, g in enumerate(genres, 1):
        print(f"{Fore.CYAN}{i}. {g}")
    print()
    while True:
        x = input(Fore.YELLOW + "Enter genre number or name: ").strip()
        if x.isdigit() and 1 <= int(x) <= len(genres):
            return genres[int(x) - 1]
        x = x.title()
        if x in genres:
            return x
        print(Fore.RED + "Invalid input. Try again.\n")

def get_rating():
    while True:
        x = input(Fore.YELLOW + "Enter minimum IMDB rating (0-10) or 'skip': ").strip()
        if x.lower() == "skip":
            return None
        try:
            r = float(x)
            if 0 <= r <= 10:
                return r
            print(Fore.RED + "Rating out of range. Try again.\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Try again.\n")

print(Fore.BLUE + "🎥 Welcome to your Personal Movie Recommendation Assistant! 🎥\n")
name = input(Fore.YELLOW + "What's your name? ").strip()
print(f"\n{Fore.GREEN}Hi {name}, choose an option:\n")
while True:
    print(Fore.CYAN + "1. AI-based Recommendation")
    print(Fore.CYAN + "2. Random Recommendation")
    opt = input(Fore.YELLOW + "Enter 1 or 2: ").strip()
    if opt == '1':
        genre = get_genre()
        mood = input(Fore.YELLOW + "How do you feel today? (Describe your mood): ").strip()
        print(Fore.BLUE + "\nAnalyzing mood", end="", flush=True)
        dots()
        mp = TextBlob(mood).sentiment.polarity
        md = "positive 😊" if mp > 0 else "negative 😞" if mp < 0 else "neutral 😐"
        print(f"\n{Fore.GREEN}Your mood is {md} (Polarity: {mp:.2f}).\n")
        rating = get_rating()
        print(f"{Fore.BLUE}\nFinding a movie for {name}", end="", flush=True)
        dots()
        rec = recommend(genre=genre, mood=mood, rating=rating, n=1)
        if isinstance(rec, str):
            print(Fore.RED + rec)
        else:
            show(rec[0])
    elif opt == '2':
        print(f"{Fore.BLUE}\nFinding a random movie for {name}", end="", flush=True)
        dots()
        rec = df.sample(n=1).iloc[0]
        pol = TextBlob(rec['Overview']).sentiment.polarity
        show((rec['Series_Title'], rec['Genre'], rec['Overview'], rec['IMDB_Rating'], pol))
    else:
        print(Fore.RED + "Invalid option. Try again.\n")
        continue
    while True:
        a = input(Fore.YELLOW + "\nWant another recommendation? (yes/no): ").strip().lower()
        if a == "no":
            print(Fore.GREEN + f"\nEnjoy your movies, {name}! 🎬🍿\n")
            exit()
        elif a == "yes":
            break
        else:
            print(Fore.RED + "Invalid choice. Try again.\n")
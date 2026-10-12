# Sentiment Spy with Report

positive = 0
negative = 0
neutral = 0

good_words = ["good", "great", "happy", "love", "awesome", "nice"]
bad_words = ["bad", "sad", "hate", "angry", "terrible", "worst"]

print("Sentiment Spy started! Type 'exit' to end.\n")

while True:
    text = input("You: ").lower()
    
    if text == "exit":
        break

    good = any(w in text for w in good_words)
    bad = any(w in text for w in bad_words)

    if good and not bad:
        print("Bot: POSITIVE 😊")
        positive += 1
    elif bad and not good:
        print("Bot: NEGATIVE 😞")
        negative += 1
    else:
        print("Bot: NEUTRAL 😐")
        neutral += 1

# Generate report
report = f"""Mission Report:
Positive messages: {positive}
Negative messages: {negative}
Neutral messages: {neutral}
"""

print("\n" + report)


import json

SPAM_KEYWORDS = ["lottery", "win", "free", "prize", "click here"]
INPUT = "data/emails.json"
OUTPUT = "data/emails_tagged.json"

def is_spam(email):
    text = (email["subject"] + " " + email["body"]).lower()
    return any(word in text for word in SPAM_KEYWORDS)

def main():
    emails = json.load(open(INPUT))
    for e in emails:
        e["spam"] = is_spam(e)
    json.dump(emails, open(OUTPUT, "w"), indent=2)
    print(f"Tagged {len(emails)} emails. See {OUTPUT}.")

if __name__ == "__main__":
    main()

def classify_query(query: str):
    query = query.lower().strip()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if query in greetings:
        return "greeting"

    return "rag"
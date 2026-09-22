def build_context(documents):
    context="\n\n".join(
        doc.page_content for doc in documents
    )
    return context

def build_prompt(context,query):
    prompt=f"""
You are a helpful customer support assistant
Answer the user's question using only the information provided in the context.

If the answer is not present in the context, say:
"I don't have enough information to answer that."

context:
{context}

User Question:
{query}

Answer:
"""
    return prompt

def generate_answer(llm, prompt):

    response = llm.invoke(prompt)

    return response.content
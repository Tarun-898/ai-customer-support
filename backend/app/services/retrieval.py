# def retrieve_documents(vector_store,query):
#     results=vector_store.similarity_search(
#         query,k=3
#     )
#     return results

import sys

sys.stdout.reconfigure(encoding="utf-8")


def retrieve_documents(vector_store, query, company_id):
    results = vector_store.max_marginal_relevance_search(
        query,
        k=3,
        fetch_k=10,
        filter={"company_id": company_id}
    )

    return results
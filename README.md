# AI Customer Support Assistant

A production-oriented **B2B AI Customer Support Assistant** built using **Retrieval-Augmented Generation (RAG)**.

The system allows companies to upload their own PDF documents and provides an AI-powered chat interface that answers customer questions using only the information available in the company's uploaded documents.

The application is designed with **multi-tenant document isolation**, so one company's documents are not used to answer another company's questions.



##  Live Demo

**Production API:**
https://ai-customer-support-q3pu.onrender.com

**Swagger API Documentation:**
https://ai-customer-support-q3pu.onrender.com/docs


#  Project Overview

Traditional customer support systems usually depend on manually maintained FAQs or fixed responses.

This project uses **RAG (Retrieval-Augmented Generation)** to dynamically retrieve relevant information from company documents and provide context-aware answers.

A company can:

1. Upload a PDF document.
2. The document is extracted and split into smaller chunks.
3. Chunks are converted into vector embeddings.
4. Embeddings are stored in ChromaDB.
5. A customer asks a question.
6. The question is converted into an embedding.
7. Relevant document chunks are retrieved.
8. Retrieved information is passed to an LLM.
9. The LLM generates the final answer.

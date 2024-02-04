# What is Haystack 🔥🔥
___
Haystack is an end-to-end framework that you can use to build powerful and production-ready pipelines with Large Language Models (LLMs) for different search use cases. 

### ⌛ Usage
perform retrieval-augmented generation (RAG), question answering, or semantic document search, you can use the state-of-the-art LLMs and NLP models in Haystack to provide custom search experiences and make it possible for your users to query in natural language. 

### 🔨 The Building Blocks of Haystack
There are a lot of components you can use to build Haystack search systems:
- **Node**
    - it performs different kinds of tasks such as: Preprocessing data, Retrieving documents, Answering questions, Summarizing documents and Routing data.
    - These are often powered by the latest LLMs and transformer models.
- **Pipeline**
    - They connect these individual nodes in a specific order to accomplish a particular NLP task. 
    - it has different types:
        - Querying Pipelines: 
            - it is used to receive a query from the user and produce a result. They have access to a DocumentStore which stores a set of documents.
        - Indexing Pipelines
            - it is used to prepare your files for search. Their main objective is to convert your files into Haystack Documents, so that they can be saved in a DocumentStore.
- **Agent**
    - Agents are essentially LLMs equipped with a set of tools (which can be pipelines or individual Haystack nodes).
    - They are used to tackle complex tasks far beyond simple pipelines.
    - Unlike pipelines, which follow a fixed sequence of steps, agents work iteratively through a decision-making process.
    - They use the LLM's ability to generate text and understand prompts to:
        - Break down complex questions into smaller, actionable steps.
        - Choose the right tool for each step based on their understanding of the information and previous results.
        - Generate appropriate inputs for the chosen tool.
        - Interpret the output from the tool to decide if they have the answer or need to repeat the process.
    - Usage:
        - Handle multi-hop question answering: <br>
        They can combine information from multiple sources and steps to answer complex questions that require reasoning and analysis.
        - Flexibility and adaptability: <br>
        You can create custom tools and configure agents to fit specific needs and domains.


### 📢 Haystack Retriever vs Reader
| Feature       | Retriever                                          | Reader                                       |
|---------------|----------------------------------------------------|----------------------------------------------|
| Function      | Find relevant documents                            | Extract answer from documents               |
| Input         | User query                                         | Retrieved documents                         |
| Output        | List of documents                                  | Answer to the question                      |
| Methods       | Keyword matching, embeddings, semantic search      | Rule-based, machine learning, LLM-based     |
| Focus         | Efficiency and speed                               | Accuracy and precision                      |
| Complexity    | Relatively simpler                                 | More computationally expensive              |
| Examples      | Elasticsearch Retriever, Embedding Retriever        | FARM Reader, Transformers Reader            |

**Summary:**
- Retrievers act like librarians, scanning through a vast collection of books to find relevant ones based on your request.
- Readers serve as expert analysts, carefully examining those books to pinpoint the specific information you need.
# Semantic Caching Rate Limiting Demo

1. Go over PowerPoint
2. Show `lab-semantic-caching` resource group
3. Show `foundry1-yjtp3yjn5hcpa`
   - Briefly explain Foundry
   - Show the chat completions / embedding model
   - Show deploying a new model
4. Show Azure APIM
   - Brief overview of API section
     1. Many operations but only these ones being used:
        - `POST /deployments/{deployment-id}/chat/completions`
        - `POST /deployments/{deployment-id}/embeddings`
     2. Go over the policy
   - Show backends
     - `Embeddings-backend`
     - `Foundry1`
5. Go through Jupyter notebook
   - Run through it as is
   - Run `check-redis-cache.py`
     - Show vector representation / prompt storage
     - Show that only one prompt is stored
   - Run `clear-redis-cache.py`
   - Change APIM threshold score to **0.05**
   - Run `check-redis-cache.py`
     - Show vector representation / prompt storage
     - Show that four prompts are stored
   - Run `clear-redis-cache.py`

# Rate Limiting Demo

1. Go over PowerPoint  
2. Show policy in VS Code  
3. Run through Jupyter Notebook

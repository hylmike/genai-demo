# genai-demo
- This is simple AI assistant app powered by Generative AI (ChatGPT) and RAG (Retrieval Augmented Generation)
- This AI assistant can remember your chat history and some knowledge we imported in vector database based on info from Syntax website (I just used one page text for demo purpose)
- The app is equipped with authentication, based on simple OAuth2 auth (username & password) in beginning and JWT later

## Frontend
- Frontend use React framework, just built a simple UI with login and AI Assistant page
- You need add '.env' file in 'frontend' folder for API url config, content can refer to env-example file

## Backend
- Backend use Python FastAPI framework, DB use postgres, vector store use Chroma, based on full async mode with test performance
- As backend use docker to set up api and database, you need docker pre-installed in your mathine
- You need add '.env' file in 'backend' folder for some DB and secret config, content can refer to env-example file
- As this app use Open AI ChatGPT, you also need OPAI_API_KEY ready to run the app. Key is configured in backend '.env' file

## Testing
- In root folder run 'npm run dev:backend' to start backend, which will set up API and DB in docker
- First run 'npm install' command to install all dependencies in frontend folder. Then in root folder run 'npm run dev:frontend' to start frontend, you need log in to test service. Url to access app locally is:
    - http://localhost:4000/
- For testing purpose, I have inserted a admin uesr with following config"
    - username: admin
    - password: 54321
- As backend use FastAPI, you also can access all API endpoints and docs with this local url:
    - http://localhost:3100/docs

## Others
- Due to time limitation, I have not added any tests, also comments in app may not enough. But this can be added easily later on if required
- Same due to time limitation, I have not added full error handling part in app (front & backend), now just some basic parts. If we want this app to be production ready, still need add more in this part

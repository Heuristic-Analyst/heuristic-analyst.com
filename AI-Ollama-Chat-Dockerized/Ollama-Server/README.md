You just need windows with nvidia drivers installed and the Docker-compose.yml file

open cmd in the project folder witht he yml file, type in:
docker compose up -d

this will build and run the container ready with Ollama port mapping 11434 to host 11434

The models will be saved in the new created folder "ollama_models"

When stopping the container:
docker compose stop

To Restart after stopping:
Docker compose start

To stop and delete container:
docker compose down

Download a model: Since the container is fresh, you'll need to "pull" a model once. Run this in your terminal:
docker compose exec -it ollama ollama run llama3

**OR in my case:**
docker compose exec -it ollama ollama run glm-4.7-flash:q8_0

Check your folder: You will notice a new folder named ollama_models appearing in your directory. Don't delete this! That's where your Llama 3 files now live on your Windows drive.


Of couse your terminals path should be open in this directory where the yml file is! Otherwise the docker compose commands do not work!

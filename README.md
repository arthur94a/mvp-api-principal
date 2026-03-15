# Dockerfile

## Montar imagem
```
docker build -t mvp_api_principal .  
```

## Executar imagem com volume:
``` 
docker run -p 8000:8000 -v $(pwd)/database:/app/database m
vp_api_principal
```


# Virtualenv

## Criar virtualização
```
virtualenv venv
```


## Ativar virtualização 
### Linux/Mac
```
source venv/bin/activet
```
### Windows
```
venv\Scripts\activet
```

# Run server
```
uvicorn main:app --reload
```
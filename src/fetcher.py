import requests
import os

running = True

while running:
    with open('fetcher.conf', 'r') as f:
        action = f.readline() # extraemos el stop
        if action[-1] == '\n': #quitamos salto de linea si existe para que la primera linea se simplemente igual a stop
            action = action[:-1]
    if action == 'stop':
        running = False
    queue = os.listdir('fetcher-queue')#extraemos el contenido de la cola del fetcher
    explored = set(os.listdir('fetcher-explored'))#extraemos el contenido de las url ya explorados
    
    for item in queue:
    
        if item in explored:# si ya hemos extraido el html de esa url
            os.remove('fetcher-queue/'+item) # lo quitamos de la cola de fetcher y seguimos
            continue # volvemos al principio del bucle
            
        with open('fetcher-queue/'+item, 'r') as f: # abrimos el archivo con la url 
            url = f.readline()# cogemos la url de la primera linea del archivo
            if url[-1] == '\n':
                url = url[:-1]
        
        html_content = requests.get('https://www.skysports.com'+url).text # hacemos la petición http de la url
        
        with open('parser-queue/'+item, 'w') as f:
            f.write(html_content) #carcagamos en la cola del parser el fichero html descargado
            
        with open('fetcher-explored/'+item, 'w') as f:
            f.write(html_content) #guardamos una copia del html en la carpeta fetcher explorer

        explored = explored.union({item})#añadimos a las url ya exploradas, la de esta iteracción
        
        os.remove('fetcher-queue/'+item)# quitamos la url de la cola del fetcher
from bs4 import BeautifulSoup
import re
import os

running = True

def to_filename(s):# función para convertir las url en nombres de archivo
    return s.replace('-', '--').replace('/','-')

def get_table(table, output_file, competition):#función para extraer las tablas del archivo con el contenido html. Parametros: tabla a extraer y archivo donde se va escribir 
    for team in table.find_all('tbody'):
        rows = team.find_all('tr') # las filas de cada tabla llevan la cabecera tr
        for row in rows:#extraemos los campos de la tabla
            pl_team = row.find('td', class_ = 'standing-table__cell standing-table__cell--name').text.strip() #nombre del equipo de futbol
            pl_pi = row.find_all('td', class_= 'standing-table__cell')[2].text #texto de los partidos jugados
            pl_w = row.find_all('td', class_= 'standing-table__cell')[3].text  #texto de los partidos ganados
            pl_d = row.find_all('td', class_= 'standing-table__cell')[4].text  #texto de los partidos empatados
            pl_l = row.find_all('td', class_= 'standing-table__cell')[5].text  #texto de los partidos perdidos
            pl_f = row.find_all('td', class_= 'standing-table__cell')[6].text  #texto de los goles a favor
            pl_a = row.find_all('td', class_= 'standing-table__cell')[7].text  #texto de los goles en contra
            pl_gd = row.find_all('td', class_= 'standing-table__cell')[8].text #texto de la diferencia de goles
            pl_pts = row.find_all('td', class_= 'standing-table__cell')[9].text #texto de los puntos que lleva cada equipo
            output_file.write('{},{},{},{},{},{},{},{},{},{}\n'.format(competition,pl_team,pl_pi,pl_w,pl_d,pl_l,pl_f,pl_a,pl_gd,pl_pts))
            

while running:
    with open('parser.conf', 'r') as f:
        action = f.readline() # extraemos el stop
        if action[-1] == '\n': #quitamos salto de linea si existe para que la primera linea se simplemente igual a stop
            action = action[:-1]
    if action == 'stop':
        running = False
    queue = os.listdir('parser-queue')#extraemos el contenido de la cola del parser

    for item in queue:
        if len(item) > 7 and item[-6:] == '-final':# si los archivos acan en el sufijo -final
            with open('parser-queue/'+item, 'r') as f:
                html = f.read()
            bs = BeautifulSoup(html, 'html.parser') #parseamos el html

            tables = bs.find_all('table', class_ = 'standing-table__table callfn') # buscamos la/s tabla/s
            
            with open('output/'+item,'w') as output_file:#abrimos el archivo donde va a ir la tabla final
                for t in tables:
                    get_table(t, output_file, t.find('caption').string.strip())# llamamos al método que extrae las tablas y las escribe en el fichero

            
        else:
            with open('parser-queue/'+item, 'r') as f: 
                html = f.read() # leemos el archivo de la cola
            bs = BeautifulSoup(html, features='html.parser') #parseamos dicho html
            
            links = bs.findAll('div', {'class':"page-filters__filter"})# extraemos todos los links que hay en el botón de filtros
            
            # aqui hay que controlar las excepciones por si solo hay una de enlaces
            if links[0].text.find('Select a competition') == -1: #si no se ha encontrado la cabecera de los links de las distintas temporadas de la competición
                table_links = [it.attrs['href'] for it in links[0].findAll('a')]# enlaces a la tabla en diferentes años
                section_links = [it.attrs['href'] for it in links[1].findAll('a')]# enlaces de las demás competiciones
            else:
                table_links = [it.attrs['href'] for it in links[1].findAll('a')]# enlaces a la tabla en diferentes años
                section_links = [it.attrs['href'] for it in links[0].findAll('a')]# enlaces de las demás competiciones

            for link in section_links:
                with open('fetcher-queue/'+to_filename(link), 'w') as f:# cargamos en la cola del fetcher las competiciones decubiertas
                    f.write(link)
                    
            for link in table_links:
                with open('fetcher-queue/'+to_filename(link)+'-final', 'w') as f:# cargamos en la cola del fetcher las temporadas de la competición actual con el sufijo final
                    f.write(link)
            
        
        os.remove('parser-queue/'+item)


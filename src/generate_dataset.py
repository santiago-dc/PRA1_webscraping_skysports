import os

files = os.listdir('output')

with open('../dataset/football_competitions.csv', 'w') as o:
    o.write('competition, pl_team, pl_pi, pl_w, pl_d, pl_l, pl_f, pl_a, pl_gd, pl_pts\n')
    for file in files:
        with open('output/'+file) as i:
            o.write(i.read())
Structure From Motion Tester
============================

### Description

SFMTest est un ensemble de programme pour faire des tests sur la SFM. La structure est la suivante. Il permet de créer des environnements de tests rapide avec des piges de photos aléatoire d'un dataset. Il test sur VisualSFM et sur OpenMVG.

##### Tester

- sfmtest.py : lanceur de test principal

##### Analyser 

- crawldata.py : Trace le graphique de certaines variables d'un environnement de test (Seulement VisualSFM)
- readlog.py : creuse les logs des programmes (Seulement VisualSFM)
- get_depth_map.py : Fait la carte de profondeur à partir de la reconstruction dense (Seulement OpenMVG)

##### Divers

- correctnvm.py : correction des .nvm lors de corruption avec VisualSFM 

### Dépendances

##### Python
- Python 3.5
- PIL : https://pypi.python.org/pypi/Pillow/2.2.1
- numpy : http://www.numpy.org/
- scipy : https://www.scipy.org/
- matplotlib : http://matplotlib.org/
- plyfile : https://pypi.python.org/pypi/plyfile

##### Externes
- openMVG : https://github.com/openMVG/openMVG
- CMVS/PMVS : http://www.di.ens.fr/pmvs/ (Guide d'installation : http://adinutzyc21.blogspot.ca/2013/02/installing-bundler-on-linux-tutorial.html)
- VisualSFM : http://ccwu.me/vsfm/

### Mise en place

1. Installer toutes les dépendances de python avec pip
2. Installer openMVG et mettre tout ses programmes dans le PATH
3. Installer CMVS et PMVS et s'assurer que tous les programmes sont dans le PATH
4. Installer VisualSFM et s'assurer que tous les programmes sont dans le PATH
5. Ajouter la camera test model test avec la bonne valeur de camera width dans la liste de camera width de openMVG
6. Changer la distance focale dans les scripts au besoin

### Manuel

##### OpenMVG

Pour partir un test avec openMVG il suffit de faire :

```shell
python sfmtest.py -O <\chemin-vers-dataset\> <\nb-de-photos\>
```

**Sortie importantes du programme :**
- /results/reconstruction\_global/robust\_colorized.py : meilleure reconstruction légère
- /results/reconstruction\_global/sfm\_data.json : données du sfm
- /results/reconstruction\_global/PMVS/models/pmvs\_options.txt.ply : reconstruction dense

Le programme créera un environnement dans la RAM temporairement (/dev/shm) et copiera l'environnement dans le dossier courant à la fin des tests. Pour afficher la carte de profondeur ensuite, il suffit de faire :

```shell
python get_depth_map.py <\chemin-vers-environnement\>
```

**Sortie du programme :**
- Affiche la reconstruction dense à l'aide de matplotlib, peut être enregistrée ensuite  

##### VisualSFM

Pour partir un test avec VisualSFM il suffit de faire :

```shell
python sfmtest.py -V <\chemin-vois-dataset\> <\nb-de-photos\>
```

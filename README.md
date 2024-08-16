# sistematicreviem

This project aims to extract bibtexfiles and exort all them into a csv easing the task of sistematic reviews, 
done AI assisted

to install pip localy use
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```
The first thing to do is acces the extract scholar and put in it the desired query, its recomended use a query that 
extract less than 1000 results from googlescholar

second thing is go to all portals where you want to serach and extract from them the bibtex of your search and put then
in bibtex folder

after this create the results folder and execute the removeduplicates.py 
ajust removebylanguageandabstract to your needs and execute it. If you want filter some type of domain of result you can modify
the nobooks to it. Adjust the rankwithllm to use the term you want to rank in the search.
Modify classify to pontuate your results as you wish and modify the cut note
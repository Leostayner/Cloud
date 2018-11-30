import sys
import requests
import json

#edp = 'http://52.207.226.119:5000/Tarefas/'

edp = "http://18.207.126.190:5000/Tarefas/"
## 1 - tarefa adicionar 2 - titulo 3 - desc

if(sys.argv[1]) == "ed":
    r = requests.get(edp)
    print(r.status_code)
    

elif (sys.argv[1]) == "tarefa adicionar":
    data = {"title": sys.argv[2], "description": sys.argv[3]}
   
    r = requests.post(edp, json = data)
    print(r.text)

elif (sys.argv[1]) == "tarefa listar":
    r = requests.get(edp)
    print(r.text)
    
elif (sys.argv[1]) == "tarefa buscar":
    arg_id = sys.argv[2]
    r = requests.get(edp + str(arg_id))
    print(r.text)
    
elif (sys.argv[1]) == "tarefa apagar":
    arg_id = sys.argv[2]
    r = requests.get(edp + str(arg_id))
    print(r.text)
    
elif (sys.argv[1]) == "tarefa atualizar":
    data = {"title": sys.argv[2], "description": sys.argv[3]}
    r = requests.get(edp , json = data)
    print(r.text)
    
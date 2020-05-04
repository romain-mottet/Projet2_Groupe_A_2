from flask import Flask, render_template , request
from flask import abort, redirect, url_for


app = Flask(__name__)
import sqlite3
import datetime
from datetime import date
from datetime import timedelta 
from datetime import datetime

def count_error (type , name ):

    """
    pré: type : course ou task et name = nom recherché
    post: retourne une liste lcount du nombre de [fail, success, killed, overflow, timeout, crash, error]
    """

    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()
    c.execute ("SELECT result FROM submissions WHERE {} = '{}'".format(type, name))

    info = c.fetchall()
    
    liste = []
    for e in range (0, len (info)):
        newstring = ""
        for i in range (0, len (info[e])):
            if info[e][i] == "(" or info[e][i] == ")" or info[e][i] == ",":
                pass
            else:
                newstring += str (info[e][i])
        liste.append (newstring)
    
    lcount = []
    fail = 0
    success = 0
    killed = 0
    overflow = 0
    timeout = 0
    crash = 0
    error = 0
    for count in range (0, len (liste)):
        if liste [count] == 'failed':
            fail+= 1
        
        elif liste [count] == 'success':
            success +=1
        
        elif liste [count] == 'killed':
            killed +=1

        elif liste [count] == 'overflow':
            overflow +=1

        elif liste [count] == 'timeout':
            timeout +=1
        
        elif liste [count] == 'crash':
            crash += 1
        
        elif liste [count] == 'error':
            error +=1

    lcount.append (fail)
    lcount.append (success)
    lcount.append (killed)
    lcount.append (overflow)
    lcount.append (timeout)
    lcount.append (crash)
    lcount.append (error)
    conn.close()
    return lcount
 
def info_course (name):
    """
    pré: Le nom du cours en générale
    post: return une liste sous la forme [nombre de réussite globale du cours, nombre de fail globale du cours, nombre d'essaye total, nombre d'essaye moyen, countsumissions]
    """
    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()

    lcourse= []

    #trouve le nombre de réussite globale 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'true'".format(name))
    r_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    lcourse.append (r_global)

    #Trouve le nombre de ratés de cours 
    c.execute ("SELECT * FROM user_tasks WHERE course = '{}' and succeeded = 'false'".format(name))
    f_global = len(c.fetchall())   #info qui devrait être introduit dans le graphe
    lcourse.append (f_global)

    #Trouve le nombre d'essaye total
    c.execute ("SELECT tried FROM user_tasks WHERE course = '{}'".format(name))
    tried = c.fetchall ()
    nbr_tried = 0
    for e in range (0, len (tried)):
        newstring = ""
        for i in range (0, len (tried [e])):
            if tried [e][i] == "(" or tried [e][i] == ")" or tried [e][i] == ",":
                "nothing"
            else:
                newstring += str (tried [e][i])
        nbr_tried += int (newstring)
    lcourse.append (nbr_tried)

    
    #trouve le nombre d'essaye moyen 
    if (lcourse[0]+lcourse[1]) !=0 :
            moyenne_tried = nbr_tried //(lcourse[0]+lcourse[1])
            lcourse.append (moyenne_tried)
    else :
            lcourse.append (None)
    
    lcourse.append (count_error('course', name))

    conn.close()
    return lcourse  

def info_task (tache):
    """
    pré: Le nom de la tache 
    post: return une liste sous la forme [nom du cours où elle se trouve,nombre de réussite, nombre d'échec , nombre d'essaye total, nombre d'essaye moyen, note à la meilleure sumissions sous forme de liste, countsubmission ]
    """
    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()

    ltache = []

    #trouve le cours où est la tâche
    c.execute ("SELECT course FROM user_tasks WHERE task = '{}'".format(tache))
    cours = c.fetchone()
    if cours == None :
            return None
    else:
        name = ""
        for i in range (0, len (cours)):
                if cours [i] == "(" or cours [i] == ")" or cours [i] == ",":
                    "nothing"
                else:
                    name += str (cours[i])
        ltache.append (name)
        
        #trouve le nombre de réussite de la tache
        c.execute ("SELECT * FROM user_tasks WHERE task = '{}' and succeeded = 'true'".format(tache))
        r_tache = len (c.fetchall ())
        ltache.append (r_tache)


        #trouve le nombre d'échec de la tache
        c.execute ("SELECT * FROM user_tasks WHERE task = '{}' and succeeded = 'false'".format(tache))
        f_tache = len (c.fetchall ())
        ltache.append (f_tache)


        #trouve le nombre d'essaye de la tâche 
        c.execute ("SELECT tried FROM user_tasks WHERE task = '{}'".format(tache))
        tried = c.fetchall ()
        nbr_tried = 0
        for e in range (0, len (tried)):
            newstring = ""
            for i in range (0, len (tried [e])):
                if tried [e][i] == "(" or tried [e][i] == ")" or tried [e][i] == ",":
                    "nothing"
                else:
                    newstring += str (tried [e][i])
            nbr_tried += int (newstring)
        ltache.append (nbr_tried)


        #trouve le nombre moyen d'essaye par étudiant 
        if (ltache[1]+ltache[2]) !=0 :
                moyenne_tried = nbr_tried //(ltache[1]+ltache[2])
                ltache.append (moyenne_tried)
        else :
                ltache.append (None)


        #trouve la note à la meilleure soumission
        c.execute ("SELECT grade FROM user_tasks WHERE task = '{}'".format(tache))
        res = c.fetchall()
        lclean = []
        for i in range (0, len (res)):
            newstring =""
            for e in range (0, len(res[i])):
                if res[i][e] == '(' or res[i][e] == '(' or res[i][e] == ',':
                    pass
                else:
                    newstring += str (res[i][e])
            lclean.append (float(newstring))

        temp = [0,0, 0, 0, 0, 0,0, 0, 0, 0 ]
        for count in range (0, len(lclean)):
            flag = False
            a = 0
            b = 10
            c = 0
            while flag != True:
                if a <= lclean[count] < b or (a == 90 and lclean[count] ==  100):
                    temp [c]= temp[c]+1
                    flag = True

                
                else :
                    a += 10
                    b+= 10
                    c += 1
        ltache.append (temp)


        ltache.append (count_error('task', tache))

        conn.close()
        return ltache 


def submitted_on_day (type, name):

    """
    pré: type est soit course or task / name est le nom de la tâche ou du cours sous forme d'un string
    post : return in dictionnaire où la clé est la date de la sumission et le résultat est le nombre de soumissions ce jour là
    """

    conn = sqlite3.connect ('inginious.sqlite')
    c = conn.cursor ()
    c.execute ("SELECT SUBSTR(submitted_on, 0, 11) FROM submissions WHERE {} = '{}'ORDER BY submitted_on ".format(type, name))
    content = c.fetchall()
    d = {}
    for i in range (len (content)):
        try:
            d[content[i][0]] = d[content[i][0]] + 1
        
        except :
            d[content[i][0]] = 1

    return d

def submitted_on_week (type, name):

    """
    pré: type est soit course or task / name est le nom de la tâche ou du cours sous forme d'un string
    post: dictionnaire où la clé est un string s suivit du numéro de la semmaine, et le résultats le nombre soumissions
    """
    dic = submitted_on_day (type, name)
    a = -7
    janv_1 = date(2019,1,1)
    dic2 = {}
    for key, value in dic.items ():
        keydate = datetime.fromisoformat(key)
        temp = keydate.timetuple()
        num_day = temp[7]
        if a <= num_day < a+7:
            dic2 [name] = dic2 [name]+ value
        else:
            while not (a <= num_day < a+7):
                formated_date1 = "{}-{}-{}".format (janv_1.year,janv_1.month,janv_1.day)
                later = janv_1 + timedelta(days=7)
                formated_date2 = "{}-{}-{}".format(later.year,later.month, later.day)
                a +=7
                if a > 365:
                    a = 0
                if a <= num_day < a+7:
                    dic2 ["{} au {}".format(formated_date1,formated_date2)] = value
                else:
                    if dic2 == {}:
                        pass
                    else:
                        dic2 ["{} au {}".format(formated_date1,formated_date2)] = 0
                name = "{} au {}".format(formated_date1,formated_date2)
                janv_1 = janv_1 + timedelta(days=7)
            
    return dic2

def sub_week_list (type, name):
    dic = submitted_on_week (type, name)
    final_list = []
    key_list = []
    value_list = []
    for key, value in dic.items ():
        key_list.append (key)
        value_list.append (value)
    if len (value_list) != len (key_list):
        raise ValueError
    else:
        final_list.append (key_list)
        final_list.append (value_list)
        return final_list


@app.route('/')
def index():
        return render_template("index.html")

@app.route('/LSINF1252', methods= ['POST', 'GET'])
def LSINF1252( infocourse = None, name_task = None , infotache = None, name = None, sub_info = None):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LSINF1252":
                                return render_template("infotache.html", infocourse = info_course ('LSINF1252'), name_task = nom, infotache = ltache, sub_info = sub_week_list ("task",nom))
                        else:
                                return render_template("cours.html", infocourse = info_course ('LSINF1252'), name_task = "Cette tâche ne  fait pas partie du cours LSINF1252 " , infotache = ['', 0, 0, 0, 0, [0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], name = 'LSINF1252' )
                
                else:
                        return render_template("cours.html", infocourse = info_course ('LSINF1252'), name_task = "Cette têche n'existe pas" , infotache = ['', 0, 0, 0, 0, [0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], name = 'LSINF1252' )  


        return render_template("cours.html", infocourse = info_course ('LSINF1252'), infotache = ['', 0, 0, 0, 0, [0, 0, 0, 8, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0]], name = 'LSINF1252' )




@app.route('/LEPL1402', methods= ['POST', 'GET'])
def LEPL1402( infocourse = None, name_task = None , infotache = None, name = None, sub_info = None):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LEPL1402":
                                return render_template("infotache.html", infocourse = info_course ('LEPL1402'), name_task = nom , infotache = ltache, sub_info = sub_week_list ("task",nom))
                        else:
                                return render_template("cours.html", infocourse = info_course ('LEPL1402'), name_task = "Cette tâche ne  fait pas partie du cours LEPL1402 ", name = 'LEPL1402' )
                
                else:
                        return render_template("cours.html", infocourse = info_course ('LEPL1402'), name_task = "Cette têche n'existe pas" , name = 'LEPL1402')  


        return render_template("cours.html", infocourse = info_course ('LEPL1402'), name = 'LEPL1402')



@app.route('/LSINF1101_PYTHON', methods= ['POST', 'GET'])
def LSINF1101_PYTHON( infocourse = None, name_task = None , infotache = None, name = None, sub_info = None):
        if request.method == 'POST':
                nom = request.form.get ("name_tache")
                ltache = info_task (nom)
                if info_task (nom) != None :
                        if ltache [0] == "LSINF1101-PYTHON":
                                return render_template("infotache.html", infocourse = info_course ('LSINF1101-PYTHON'), name_task = nom , infotache = ltache, sub_info = sub_week_list ("task",nom))
                        else:
                                return render_template("cours.html", infocourse = info_course ('LSINF1101-PYTHON'), name_task = "Cette tâche ne  fait pas partie du cours LSINF1101-PYTHON ", name = 'LSINF1101-PYTHON' )
                
                else:
                        return render_template("cours.html", infocourse = info_course ('LSINF1101-PYTHON'), name_task = "Cette têche n'existe pas" , name = 'LSINF1101-PYTHON')  


        return render_template("cours.html", infocourse = info_course ('LSINF1101-PYTHON'), name = 'LSINF1101-PYTHON')

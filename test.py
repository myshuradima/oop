import cx_Oracle
import classes

connection = cx_Oracle.connect("OOPDB/Optiquest22@localhost:1521/xe")
curs = connection.cursor()
number = 6

query = 'SELECT * FROM LETTERS_PACKAGES WHERE CURRENT_LOCATION = ' + str(number)
print(query)
curs.execute(query)
letter_data = curs.fetchall()
"print(letter_data)"
letter_list = [classes.Letter(el[0], el[1], el[2], el[3], el[5], el[4]) for el in letter_data]


query = 'SELECT * FROM DEPARTMENTS WHERE DEPARTMENT_NUMBER = ' + str(number)
print(query)
curs.execute(query)
dept_data = curs.fetchall()
"print(dept_data)"
my_department = classes.Department(dept_data[0][4], dept_data[0][5], dept_data[0][6], dept_data[0][7],dept_data[0][0],dept_data[0][1],dept_data[0][2],dept_data[0][3])

for el in letter_list:
    query = 'SELECT CLIENT_ADRESS, CLIENT_AREA, CLIENT_CITY, CLIENT_REGION FROM CLIENTS WHERE CLIENT_ID = '+str(el.getter_id)
    curs.execute(query)
    client_data = curs.fetchall()
    "print(client_data[0][2])"
    print(el.number)

    if my_department.city == client_data[0][2]:
        if my_department.type == "post office":
            print(client_data[0][0]+ ' '+client_data[0][1]+ ' '+client_data[0][2])
        else:
            print("deliver to post office")
            print(client_data[0][0] + ' ' + client_data[0][1] + ' ' + client_data[0][2])
            query = "SELECT DEPARTMENT_NUMBER, DEPT_ADRESS FROM DEPARTMENTS WHERE DEPARTMENT_TYPE = 'post office' AND DEPT_CITY = '" + client_data[0][2] + "' AND DEPT_AREA = '" + client_data[0][1]+"'"
            curs.execute(query)
            next_dept_list = curs.fetchall()
            if(next_dept_list):
                print("deliver to post office №" + next_dept_list[0][0])
            else:
                query = "SELECT DEPARTMENT_NUMBER, DEPT_ADRESS FROM DEPARTMENTS WHERE DEPARTMENT_TYPE = 'post office' AND DEPT_CITY = '" + \
                        client_data[0][2] + "' AND FREE_VOLUME = (SELECT MAX(FREE_VOLUME) FROM DEPARTMENTS)"
                curs.execute(query)
                next_dept_list2 = curs.fetchall()
                print("deliver to post office №" + str(next_dept_list2[0][0]))
    else:
        if my_department.type == "storrage" and my_department.region == client_data[0][3]:
            query = "SELECT DEPARTMENT_NUMBER, DEPT_ADRESS FROM DEPARTMENTS WHERE DEPARTMENT_TYPE = 'post office' AND DEPT_CITY = '"+\
                    my_department.city +"' AND FREE_VOLUME = (SELECT MAX(FREE_VOLUME) FROM DEPARTMENTS)"
            curs.execute(query)
            next_dept_list2 = curs.fetchall()
            print("deliver to post office №" + str(next_dept_list2[0][0]))
        else:
            query = "SELECT DEPARTMENT_NUMBER, DEPT_ADRESS FROM DEPARTMENTS WHERE DEPARTMENT_TYPE = 'storrage' AND DEPT_REGION = '" + \
            client_data[0][3] + "'"
            curs.execute(query)
            next_dept_list2 = curs.fetchall()
            print("deliver to storrage  with number " + next_dept_list2[0][0])
curs.close()
connection.close()


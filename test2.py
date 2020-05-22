import lab3
import cx_Oracle

employee = lab3.Employee.load_from_db("login", "password")

#pack = lab3.Package.load_from_db(1)

employee.create_order('adam', 'sam',  'third street', 'third street', 'Podol', 'Solomyansky', 'Kyiv', 'Kyiv',
                      'Kyiv_obl', 'Kyiv_obl', '112-85-96', '221-85-96', 15, 20)

#client.save_to_db()
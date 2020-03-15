

from classes import Letter, Department, Client
l1 = Letter(1,"h1", "v2", 12.3, 1)
l2 = Letter(2,"h1", "v3", 12.3, 1)
l3 = Letter(3,"h1", "v1", 12.3, 1)
dept1 = Department("1", "1st-street", "1st-area", "Kyiv", "Kyiv obl", 1, "dept", 13.2, 12.4)
dept2 = Department("1", "2nd-street", "3st-area", "Lviv", "Lviv obl", 2, "dept", 13.4, 10.2)
dept3 = Department("1", "3st-street", "1st-area", "Kyiv", "Kyiv obl", 3, "storage", 13.2, 12.4)
dept4 = Department("1", "4nd-street", "3st-area", "Lviv", "Lviv obl", 4, "storage", 13.4, 10.2)
client1 = Client("h1", "name 1", "000-00-00", "2", "3-street", "3-area", "Kyiv","Kyiv obl", "sender")
client2 = Client("v1", "name 2", "000-00-00", "2", "3-street", "3-area", "Lviv", "Lviv obl" ,"getter")
client3 = Client("v2", "name 3", "000-00-00","2", "3-street", "3-area", "Lviv","Lviv obl" ,"getter")
client4 = Client("v3", "name 4", "000-00-00","2", "3-street", "3-area", "Kyiv","Kyiv obl" ,"getter")

letterslist=[l1, l2, l3]
clientlist=[client1, client2, client3, client4]
deptlist = [dept1, dept2, dept3, dept4]
l1.next_move(deptlist)
print(client1.type)
import lab2


newAdmin = lab2.Admin("AdminBob", "123-45-67", "bobs_login", "123456", 12)
newEmployee1 = newAdmin.create_employee("Adam", "123-45-67", "adams_login", "123456", 2)
newEmployee2 = newAdmin.create_employee("Bob", "123-45-67", "bobs_login", "123456", 12)

print(newEmployee2.get_name())

client1, client2, package =newEmployee1.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 13, 15)
client1, client2, package1 =newEmployee2.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City1", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 33, 25)
client1, client2, package2 =newEmployee2.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City2", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 18, 25)
client1, client2, package3 =newEmployee1.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City3", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 20, 16)
client1, client2, package4 =newEmployee1.create_order("Getter Name", "Sender Name", "Getter Adress", "Sender Adress",
                                                    "Getter Area", "Sender Area","Getter City4", "Sender City", "Getter Region",
                                                    "Sender Region", "Getter Phone", "Sender Phone", 16, 15)
print(client1.get_name())
print(client2.get_name())
print("_________________________________")
package_list=[package, package1, package2, package3, package4]
for el in package_list:
    print(el.get_current_place())
    print(newEmployee2.get_name())
    el.check(newEmployee2)
    print(el.get_current_place())

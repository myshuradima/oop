import body
pack = body.Admin.load_from_db("admin", "password")
pack.get_schedule()
print()
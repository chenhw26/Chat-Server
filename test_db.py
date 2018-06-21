import DBUsr as usr
import DBGroup as group

# print(usr.get_profile(10000))
curid1 = usr.new_usr('name', '666666')
curid2 = usr.new_usr('name2', '666666')
print(curid1, curid2)
print(usr.get_profile(curid1))
print(usr.get_profile(curid2))

usr.update_profile((curid1, 'name1', '666666', False), curid1)
print(usr.get_profile(curid1))

usr.add_friend((curid2, 'name2'), curid1)
print(usr.get_friends(curid1))
usr.del_friend(curid2, curid1)
print(usr.get_friends(curid1))

usr.add_black((curid2, 'name2'), curid1)
print(usr.get_black(curid1))
usr.del_black(curid2, curid1)
print(usr.get_black(curid1))

usr.join_group((10000, 'group'), curid1)
print(usr.get_groups(curid1))
usr.del_group(10000, curid1)
print(usr.get_groups(curid1))

usr.add_moments((10000, 'time', 'content'), curid1)
print(usr.get_moments(curid1))

usr.add_record(('name1', 'name2', 'time', 'content'), curid1, curid2)
print(usr.get_record(curid1, curid2))

usr.add_unreceived(curid1, '666666')
print(usr.get_and_clear_unreceived(curid1))
print(usr.get_and_clear_unreceived(curid1))

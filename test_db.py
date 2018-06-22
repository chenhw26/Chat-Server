import DBUsr as usr
import DBGroup as group
import unittest

class TestDBGroup(unittest.TestCase):
    def test_all(self):
        curid = group.new_group('group', 10000, 'founder')
        self.assertEqual(curid, 10005)
        self.assertEqual(group.get_profile(curid), (curid, 'group', False))
        group.update_profile(curid, (curid, 'group1', False))
        self.assertEqual(group.get_profile(curid), (curid, 'group1', False))

        self.assertEqual(group.get_mem(curid), [(10000, 'founder', True, False)])
        group.add_mem(curid, 10001, 'member')
        self.assertEqual(group.get_mem(curid), [(10000, 'founder', True, False), (10001, 'member', False, False)])
        group.del_mem(curid, 10001)
        self.assertEqual(group.get_mem(curid), [(10000, 'founder', True, False)])

        group.add_mem(curid, 10001, 'member')
        group.add_ad(curid, 10001)
        self.assertEqual(group.get_mem(curid), [(10000, 'founder', True, False), (10001, 'member', True, False)])
        group.del_ad(curid, 10001)
        self.assertEqual(group.get_mem(curid), [(10000, 'founder', True, False), (10001, 'member', False, False)])

        group.add_pingbi(curid, 10000)
        self.assertEqual(group.get_mem(curid), [
                     (10000, 'founder', True, True), (10001, 'member', False, False)])
        group.del_pingbi(curid, 10000)
        self.assertEqual(group.get_mem(curid), [
                     (10000, 'founder', True, False), (10001, 'member', False, False)])

        self.assertEqual(group.get_record(curid), [])
        group.add_record(curid, 'founder', 10000, 'time', 'content')
        self.assertEqual(group.get_record(curid), [('founder', 10000, 'time', 'content')])

unittest.main()
S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================


class Group:

    def __init__(self):
        self.members = {} # {name1: state1, name2: state2, ...}
        self.chat_grps = {} # {1: [name1, name2], 2: [a, b, c], ...}
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        '''return True if name is in members, False otherwise'''
        # ---- start your code ---- #
        pass

        return False
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system,
        remove name from members and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        pass

        # ---- end of your code --- #
        return


    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """

        found = False
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        pass

        # ---- end of your code --- #
        return found, group_key




    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)

        # IMPLEMENTATION
        # ---- start your code ---- #
        pass

        # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system

        Remove "me" from my current chat group.
        If the group has only one peer left,
        remove that peer as well, and delete the chat group.
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        pass

        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        Return the chat group which "name" is in, as a list.
        IMPORTANT: "name"  is the first element in that returning list.
        (hint: use find_group)
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        pass

        # ---- end of your code --- #
        return my_list


if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    g.members = {}
    print(g.list_all())

    g.connect('a', 'b')
    print(g.list_all())
    g.connect('c', 'a')
    print(g.list_all())
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')


    print(g.list_all())

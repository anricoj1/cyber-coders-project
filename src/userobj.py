

'''Used to hold currently logged in user'''
class user_obj:
    def __init__(self, userAttr):
        self.__user_id = userAttr[0]
        self.__fname = userAttr[1]
        self.__lname = userAttr[2]
        self.__email = userAttr[3]
        self.__pict = userAttr[6]
    def getID(self):
        return self.__user_id
    def getfirstname(self):
        return self.__fname
    def getlastname(self):
        return self.__lname
    def getEmail(self):
        return self.__email
    def getProfPic(self):
        return self.__pict
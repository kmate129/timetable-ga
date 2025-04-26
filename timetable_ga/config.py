import CourseClass
import StudentsGroup


class Configuration:

    def __init__(self):
        self.isEmpty = True
        self.professors = {}
        self.studentGroups = {}
        self.courses = {}
        self.rooms = {}
        self.courseClasses = []

    def Parsefile(self, fileName):
        self.professors = {}
        self.studentGroups = {}
        self.courses = {}
        self.rooms = {}
        self.courseClasses = []

        counter = 0
        with open(fileName) as input:
            for line in input:
                counter = counter + 1
                # get type of object, parse obect and store it
                strippedLine = line.strip()
                if strippedLine == "#group":
                    g = self.__ParseStudentsGroup(input)
                    if g:
                        self.studentGroups[g.GetId()] = g
                elif strippedLine == "#class":
                    c = self.__ParseCourseClass(input)
                    if c:
                        self.courseClasses.append(c)
        input.close()
        self.isEmpty = False

    # Reads professor's data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseStudentsGroup(self, file):
        newFile = file
        id = 0
        number = 0
        name = ""
        dictConfig = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == "#end":
                break
            key = ""
            value = ""  # noqa: F841
            p = line.find("=")
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1 :].strip()

            for key in dictConfig.keys():
                if key == "id":
                    id = dictConfig[key]
                elif key == "name":
                    name = dictConfig[key]
                elif key == "size":
                    number = dictConfig[key]

        # make object and return pointer to it
        if id == 0:
            return None
        return StudentsGroup.StudentsGroup(id, name, number)

    # Reads class' data from config file, makes object and returns pointer to it
    # Returns NULL if method cannot parse configuration data
    def __ParseCourseClass(self, file):
        newFile = file
        pid = 0
        cid = 0
        dur = 1
        lab = False
        groups = []
        dictConfig = {}
        while True:
            line = newFile.readline()
            line = line.strip()
            if line == "" or line == "#end":
                break
            key = ""
            value = ""  # noqa: F841
            p = line.find("=")
            if p != -1:
                # key
                key = line[:p].strip()
                # value
                dictConfig[key] = line[p + 1 :].strip()

            for key in dictConfig.keys():
                if key == "professor":
                    pid = dictConfig[key]
                elif key == "course":
                    cid = dictConfig[key]
                elif key == "lab":
                    lab = dictConfig[key]
                elif key == "duration":
                    dur = dictConfig[key]
                elif key == "group":
                    g = self.GetStudentsGroupById(dictConfig[key])
                    if g:
                        groups.append(g)

        # get professor who teaches class and course to which this class belongs
        p = self.GetProfessorById(pid)
        c = self.GetCourseById(cid)

        # does professor and class exists
        if not c or not p:
            return None

        # make object and return pointer to it
        return CourseClass.CourseClass(p, c, groups, lab, dur)

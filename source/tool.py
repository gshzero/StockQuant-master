
class Tool():
    def spilt_str_list(self, list_str):
        c = []
        a = list_str
        for i in a:
            i = i.replace("\'", "")
            b = i.split(',')
            c.append(b)
        return c

    def dict_statistical(self,dict_str):
        dict_list = dict_str.rstrip().split('，')

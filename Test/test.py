class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
a = {'IT': {'技术支持': 0, '故障处理': 0, '资源申请': 0}, 'HR': {'技术支持': 0, '故障处理': 0, '资源申请': 0}, 'TOP': {'技术支持': 1, '故障处理': 0, '资源申请': 0}, 'IBS': {'技术支持': 2, '故障处理': 0, '资源申请': 3}, 'ICS': {'技术支持': 0, '故障处理': 0, '资源申请': 0}}
print(a['IBS']['技术支持'])
print (a.keys())
print(list(a.keys()))
b = []
b = [{'name':'技术支持', 'data': [1,2,3,4,5]}]
new_a={'name':'技术支持',}
for wo in list(a.keys()):
    print('aa'+wo)
    print(a[wo].keys())
    key1=list(a[wo].keys())
    print(key1)
    for key2 in key1:
        print(a[wo][key2])

wo_info_tuple = (('IBS', '技术支持', 2), ('IBS', '资源申请', 3), ('TOP', '技术支持', 1))
department_list = []
wo_type_list = []
wo_dict = Vividict()
for wo_info in wo_info_tuple:
    department_list.append(wo_info[0])
    wo_dict[wo_info[0]][wo_info[1]] = wo_info[2]
    wo_type_list.append(wo_info[1])

print(wo_dict)





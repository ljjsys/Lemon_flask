#############
######Lemon_GO
框架： flask
数据库： mysql
前端：html5,css3,jquery,bootstarp

# gateone   shellinbox

# ansible

# manage the server assets
[root@mgclient ~]# dmidecode |grep Product
	Product Name: RHEV Hypervisor
[root@om-center opt]# dmidecode |grep Product
	Product Name: VMware Virtual Platform
	Product Name: 440BX Desktop Reference Platform    
    
    
1.规好好项目功能实现
2.规划好目录结构


1. 上传文件
2. web远程执行命令
3. 不同的用户级别不同的执行权限
4. 查看系统负载
5. 查看系统log

for module, url_prefix in modules:
    app.register_blueprint(module, url_prefix = url_prefix)

通过传递两个参数至register_blueprint方法注册Blueprint。根据传递过来的参数module是admin与frontend,而admin与frontend是已经定义好的Blueprint对象。url_prefix为绑定的url路径，看到这里是不是赫然开朗起来了？

举个例子，如果你需要另外加一个模块用于管理商店，那么可以通过以下几个步骤添加：
1、在views包里面新建一个shop.py，定义一个Blueprint的对象shop
2、导入到__init__.py里面。
3、在sasuke包的__init__.py中导入shop
4、DEFAULT_MODULES中添加(shop, ‘/shop’)


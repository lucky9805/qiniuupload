#要上传的空间
bucket_name = ['t-edge-video']

#域名
domain = 'http://ofadw524x.bkt.clouddn.com/'

access_key = '3v5_ke67gD22uhdxf6Si_Lty21s2drVsLwdR07NH'
secret_key = 'FSTVxNLEb50PQi1j4Ui0_sWqh8ntatKTMlfkOK80'



#安装之前需要安装qiniu的包
#python3 install -r requirements.txt

#打包成为可执行文件需要
#2.安装py2app

#pip3 install py2app
#目前原来的py2app有问题，用下面的安装
#pip3 install -U git+https://github.com/metachris/py2app.git@master
#3.生成setup文件

#py2applet --make-setup qiniu_upload.py

#4.打包

#自己开发，打包速度快。
#python3 setup.py py2app

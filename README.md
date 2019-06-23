# ximcxdm
## 西门吹雪个人网盘专下工具
    西门吹雪个人网盘地址:
    http://pan.ximcx.cn/home
    此个人网盘收录了很多安全相关的工具,数量较多,下载比较麻烦,因此该工具因势而生,加快下载速度.


## 使用前提:
    1、安装python 2.7
    2、操作系统安装wget

## 使用命令:

    python ximcxdm.py url dir
    其中
    1、ximcxdm.py 即本脚本
    2、url 下载的起始URL,本工具支持子目录下载
    3、dir 本地存放目录,建议空间大一些.

## 使用举例:
    整站:
    python ./ximcxdm.py http://pan.ximcx.cn/home/ ./tmp

    仅下载某一目录,比如渗透测试工具.
    python ./ximcxdm.py http://pan.ximcx.cn/home/home/渗透测试工具 ./tmp

## 工具版本:
    2019-06-23 v0.2 增加含特殊字符&/(/)/等目录的处理
    2019-06-22 v0.1

## 作者
    sy.z


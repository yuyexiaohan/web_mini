import socket
import re
import multiprocessing
import time
import mini_frame


class WSGIServer(object):
    def __init__(self):
        # 1. 创建套接字
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 2, 1 可以不设置，默认是这2俄国值
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 65535, 4, 1

        # 2. 绑定
        self.tcp_server_socket.bind(("", 7892))

        # 3. 变为监听套接字
        self.tcp_server_socket.listen(128)

    def service_client(self, new_socket):
        """为这个客户端返回数据"""

        # 1. 接收浏览器发送过来的请求 ，即http请求  
        # GET / HTTP/1.1
        # .....
        request = new_socket.recv(1024).decode("utf-8")
        # print(">>>"*50)
        # print(request)

        request_lines = request.splitlines()
        print("")
        print(">"*20)
        print('request_lines:', request_lines)
        """打印结果：
        request_lines: 
            ['GET /mini_frame.py HTTP/1.1', 
            'Host: 127.0.0.1:7892', 
            'Connection: keep-alive', 
            'Cache-Control: max-age=0', 
            'Upgrade-Insecure-Requests: 1', 
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/69.0.3497.100 Safari/537.36', 
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
            'Accept-Encoding: gzip, deflate, br', 
            'Accept-Language: zh-CN,zh;q=0.9', 
            'Cookie: csrftoken=XeNEgFEg7BlsE8hp9SKGbVXs0I4j5PY2N10rupEv3B5jMLpQFVs8f4MwCSmXX0mq; \
            sessionid=5bp4uzk26v87sugzrg7jhup8bhxuyj4c', 
            '']
        """

        # request_lines[0] = 'GET /mini_frame.py HTTP/1.1'
        # get post put del
        file_name = ""
        # 正则解释：是匹配以非‘/’的字符+非多个空格的字符
        ret = re.match(r"[^/]+(/[^ ]*)", request_lines[0])
        print('ret:', ret)
        # ret: <_sre.SRE_Match object; span=(0, 18), match='GET /mini_frame.py'>
        if ret:
            file_name = ret.group(1)
            print("*"*50, file_name) # *** /mini_frame.py

            if file_name == "/":
                file_name = "/index.html"

        # 2. 返回http格式的数据，给浏览器
        # 2.1 如果请求的资源不是以.py结尾，那么就认为是静态资源（html/css/js/png，jpg等）
        if not file_name.endswith(".py"):
            try:
                f = open("./html" + file_name, "rb")
            except:
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------file not found-----"
                new_socket.send(response.encode("utf-8"))
            else:
                html_content = f.read()
                # print('--------html_content---------')
                # print('html_content = f.read():', html_content) # 静态文件读取html/css/image等文件
                # print('--------html_content---------')
                # html_content返回浏览器打印结果：html-->css-->image依次转换访问返回给浏览器
                """
				>>>>>>>>>>>>>>>>>>>>
request_lines: ['GET / HTTP/1.1', 'Host: 127.0.0.1:7892', 'Connection: keep-alive', 'Cache-Control: max-age=0', 'Upgrade-Insecure-Requests: 1', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'Accept-Encoding: gzip, deflate, br', 'Accept-Language: zh-CN,zh;q=0.9', 'Cookie: csrftoken=XeNEgFEg7BlsE8hp9SKGbVXs0I4j5PY2N10rupEv3B5jMLpQFVs8f4MwCSmXX0mq; sessionid=5bp4uzk26v87sugzrg7jhup8bhxuyj4c', '']
ret: <_sre.SRE_Match object; span=(0, 5), match='GET /'>
************************************************** /
--------html_content---------
html_content = f.read(): b'<?xml version="1.0" encoding="iso-8859-1"?>\n<!DOCTYPE html\n    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<!-- /fasttmp/mkdist-qt-4.3.5-1211793125/qtopia-core-opensource-src-4.3.5/doc/src/index.qdoc -->\n<head>\n  <title>Qt 4.3: Qtopia Core Reference Documentation</title>\n  <link href="classic.css" rel="stylesheet" type="text/css" />\n</head>\n<body>\n<table border="0" cellpadding="0" cellspacing="0" width="100%">\n<tr>\n<td align="left" valign="top" width="32"><a href="http://www.trolltech.com/products/qt"><img src="images/qt-logo.png" align="left" width="32" height="32" border="0" /></a></td>\n<td width="1">&nbsp;&nbsp;</td><td class="postheader" valign="center"><a href="index.html"><font color="#004faf">Home</font></a>&nbsp;&middot; <a href="classes.html"><font color="#004faf">All&nbsp;Classes</font></a>&nbsp;&middot; <a href="mainclasses.html"><font color="#004faf">Main&nbsp;Classes</font></a>&nbsp;&middot; <a href="groups.html"><font color="#004faf">Grouped&nbsp;Classes</font></a>&nbsp;&middot; <a href="modules.html"><font color="#004faf">Modules</font></a>&nbsp;&middot; <a href="functions.html"><font color="#004faf">Functions</font></a></td>\n<td align="right" valign="top" width="230"><a href="http://www.trolltech.com"><img src="images/trolltech-logo.png" align="right" width="203" height="32" border="0" /></a></td></tr></table><h1 align="center">Qtopia Core Reference Documentation<br /><small>Qt for Embedded Linux</small></h1>\n<a name="qt-reference-documentation"></a>        <table cellpadding="2" cellspacing="1" border="0" width="100%" bgcolor="#e5e5e5">\n        <tr>\n        <th bgcolor="#a2c511" width="33%">\n        Getting Started\n        </th>\n        <th bgcolor="#a2c511" width="33%">\n        General\n        </th>\n        <th bgcolor="#a2c511" width="33%">\n        Developer Resources\n        </th>\n        </tr>\n        <tr>\n        <td valign="top">\n        <ul>\n        <li><strong><a href="qt4-3-intro.html">What\'s New in Qt 4.3</a></strong></li>\n        <li><a href="how-to-learn-qt.html">How to Learn Qt</a></li>\n        <li><a href="installation.html">Installation</a></li>\n        <li><a href="tutorial.html">Tutorial</a> and <a href="examples.html">Examples</a></li>\n        <li><a href="porting4.html">Porting from Qt 3 to Qt 4</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="aboutqt.html">About Qt</a></li>\n        <li><a href="trolltech.html">About Trolltech</a></li>\n        <li><a href="commercialeditions.html">Commercial Edition</a></li>\n        <li><a href="opensourceedition.html">Open Source Edition</a></li>\n        <li><a href="http://www.trolltech.com/developer/faqs/">Frequently Asked Questions</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="http://lists.trolltech.com">Mailing Lists</a></li>\n        <li><a href="http://www.trolltech.com/developer/community/">Qt Community Web Sites</a></li>\n        <li><a href="http://doc.trolltech.com/qq/">Qt Quarterly</a></li>\n        <li><a href="bughowto.html">How to Report a Bug</a></li>\n        <li><a href="http://www.trolltech.com/developer/">Other Online Resources</a></li>\n        </ul>\n        </td>\n        </tr>\n        <tr>\n        <th bgcolor="#a2c511">\n        API Reference\n        </th>\n        <th bgcolor="#a2c511">\n        Core Features\n        </th>\n        <th bgcolor="#a2c511">\n        Key Technologies\n        </th>\n        </tr>\n        <tr>\n        <td valign="top">\n        <ul>\n        <li><a href="classes.html">All Classes</a></li>\n        <li><a href="mainclasses.html">Main Classes</a></li>\n        <li><a href="groups.html">Grouped Classes</a></li>\n        <li><a href="annotated.html">Annotated Classes</a></li>\n        <li><a href="modules.html">Qt Classes by Module</a></li>\n        <li><a href="hierarchy.html">Inheritance Hierarchy</a></li>\n        <li><a href="functions.html">All Functions</a></li>\n        <li><a href="qtopiacore.html">Qtopia Core</a></li>\n        <li><a href="overviews.html">All Overviews and HOWTOs</a></li>\n        <li><a href="gallery.html">Qt Widget Gallery</a></li>\n        <li><a href="http://doc.trolltech.com/extras/qt43-class-chart.pdf">Class Chart</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="signalsandslots.html">Signals and Slots</a></li>\n        <li><a href="object.html">Object Model</a></li>\n        <li><a href="layout.html">Layout Management</a></li>\n        <li><a href="paintsystem.html">Paint System</a></li>\n        <li><a href="graphicsview.html">Graphics View</a></li>\n        <li><a href="accessible.html">Accessibility</a></li>\n        <li><a href="containers.html">Tool and Container Classes</a></li>\n        <li><a href="i18n.html">Internationalization</a></li>\n        <li><a href="plugins-howto.html">Plugin System</a></li>\n        <li><a href="intro-to-dbus.html">Inter-process Communication</a></li>\n        <li><a href="qtestlib-manual.html">Unit Testing Framework</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="threads.html">Multithreaded Programming</a></li>\n        <li><a href="qt4-mainwindow.html">Main Window Architecture</a></li>\n        <li><a href="richtext.html">Rich Text Processing</a></li>\n        <li><a href="model-view-programming.html">Model/View Programming</a></li>\n        <li><a href="stylesheet.html">Style Sheets</a></li>\n        <li><a href="qtnetwork.html">Network Module</a></li>\n        <li><a href="qtopengl.html">OpenGL Module</a></li>\n        <li><a href="qtsql.html">SQL Module</a></li>\n        <li><a href="qtsvg.html">SVG Module</a></li>\n        <li><a href="qtxml.html">XML Module</a></li>\n        <li><a href="qtscript.html">Script Module</a></li>\n        <li><a href="activeqt.html">ActiveQt Framework</a></li>\n        </ul>\n        </td>\n        </tr>\n        <tr>\n        <th bgcolor="#a2c511">\n        Add-ons &amp; Services\n        </th>\n        <th bgcolor="#a2c511">\n        Tools\n        </th>\n        <th bgcolor="#a2c511">\n        Licenses &amp; Credits\n        </th>\n        </tr>\n        <tr>\n        <td valign="top">\n        <ul>\n        <li><a href="http://www.trolltech.com/products/qt/addon/solutions/">Qt Solutions</a></li>\n        <li><a href="http://www.trolltech.com/products/qt/3rdparty/">Partner Add-ons</a></li>\n        <li><a href="http://qt-apps.org">Third-Party Qt Components (qt-apps.org)</a></li>\n        <li><a href="http://www.trolltech.com/support/">Support</a></li>\n        <li><a href="http://www.trolltech.com/support/training/">Training</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="designer-manual.html">Qt Designer</a></li>\n        <li><a href="assistant-manual.html">Qt Assistant</a></li>\n        <li><a href="linguist-manual.html">Qt Linguist</a></li>\n        <li><a href="qmake-manual.html">qmake</a></li>\n        <li><a href="qttools.html">All Tools</a></li>\n        </ul>\n        </td>\n        <td valign="top">\n        <ul>\n        <li><a href="gpl.html">GNU General Public License</a></li>\n        <li><a href="3rdparty.html">Third-Party Licenses Used in Qt</a></li>\n        <li><a href="licenses.html">Other Licenses Used in Qt</a></li>\n        <li><a href="trademarks.html">Trademark Information</a></li>\n        <li><a href="credits.html">Credits</a></li>\n        </ul>\n        </td>\n        </tr>\n        </table>\n    <p /><address><hr /><div align="center">\n<table width="100%" cellspacing="0" border="0"><tr class="address">\n<td width="30%">Copyright &copy; 2008 <a href="trolltech.html">Trolltech</a></td>\n<td width="40%" align="center"><a href="trademarks.html">Trademarks</a></td>\n<td width="30%" align="right"><div align="right">Qt 4.3.5</div></td>\n</tr></table></div></address></body>\n</html>\n'
--------html_content---------
>>>>>>>>>>>>>>>>>>>>
request_lines: ['GET /classic.css HTTP/1.1', 'Host: 127.0.0.1:7892', 'Connection: keep-alive', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept: text/css,*/*;q=0.1', 'Referer: http://127.0.0.1:7892/', 'Accept-Encoding: gzip, deflate, br', 'Accept-Language: zh-CN,zh;q=0.9', 'Cookie: csrftoken=XeNEgFEg7BlsE8hp9SKGbVXs0I4j5PY2N10rupEv3B5jMLpQFVs8f4MwCSmXX0mq; sessionid=5bp4uzk26v87sugzrg7jhup8bhxuyj4c', '']
ret: <_sre.SRE_Match object; span=(0, 16), match='GET /classic.css'>
************************************************** /classic.css
--------html_content---------
html_content = f.read(): b'h3.fn,span.fn\n{\n  margin-left: 1cm;\n  text-indent: -1cm;\n}\n\na:link\n{\n  color: #004faf;\n  text-decoration: none\n}\n\na:visited\n{\n  color: #672967;\n  text-decoration: none\n}\n\ntd.postheader\n{\n  font-family: sans-serif\n}\n\ntr.address\n{\n  font-family: sans-serif\n}\n\nbody\n{\n  background: #ffffff;\n  color: black\n}\n\ntable tr.odd {\n  background: #f0f0f0;\n  color: black;\n}\n\ntable tr.even {\n  background: #e4e4e4;\n  color: black;\n}\n\ntable.annotated th {\n  padding: 3px;\n  text-align: left\n}\n\ntable.annotated td {\n  padding: 3px;\n}\n\ntable tr pre\n{\n  padding-top: none;\n  padding-bottom: none;\n  padding-left: none;\n  padding-right: none;\n  border: none;\n  background: none\n}\n\ntr.qt-style\n{\n  background: #a2c511;\n  color: black\n}\n\nbody pre\n{\n  padding: 0.2em;\n  border: #e7e7e7 1px solid;\n  background: #f1f1f1;\n  color: black\n}\n\nspan.preprocessor, span.preprocessor a\n{\n  color: darkblue;\n}\n\nspan.comment\n{\n  color: darkred;\n  font-style: italic\n}\n\nspan.string,span.char\n{\n  color: darkgreen;\n}\n\n.subtitle\n{\n    font-size: 0.8em\n}\n\n.small-subtitle\n{\n    font-size: 0.65em\n}\n'
--------html_content---------

>>>>>>>>>>>>>>>>>>>>
request_lines: ['GET /images/qt-logo.png HTTP/1.1', 'Host: 127.0.0.1:7892', 'Connection: keep-alive', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept: image/webp,image/apng,image/*,*/*;q=0.8', 'Referer: http://127.0.0.1:7892/', 'Accept-Encoding: gzip, deflate, br', 'Accept-Language: zh-CN,zh;q=0.9', 'Cookie: csrftoken=XeNEgFEg7BlsE8hp9SKGbVXs0I4j5PY2N10rupEv3B5jMLpQFVs8f4MwCSmXX0mq; sessionid=5bp4uzk26v87sugzrg7jhup8bhxuyj4c', '']
ret: <_sre.SRE_Match object; span=(0, 23), match='GET /images/qt-logo.png'>
************************************************** /images/qt-logo.png
--------html_content---------
html_content = f.read(): b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x03\x00\x00\x00D\xa4\x8a\xc6\x00\x00\x00\xbaPLTE \x1b\x1f \x1c\x1f\xa7\xd09#  \xa5\xcd9\xa7\xcf9(&!%! aq+KU\'R](#\x1f n\x83.~\x981\x82\x9e2\x91\xb24\x9b\xc07\xa2\xc98*(!.."h|-01"\x98\xbb6:=$t\x8c/@G%Ta)\x83\xa02\x8e\xae4Yg*\x95\xb85]m+EL&\xa0\xc67\xa1\xc8835#NX(q\x87.r\x88/bt,\x9a\xbf6Zh*\x87\xa43\x8a\xa93ar+\xa3\xca8\x8f\xaf4x\x900o\x85.{\x950\x97\xbb6|\x961IR\'\x80\x9b1\x9d\xc27k\x7f-69#,+!\'$ 68#Ub)cu,h\xeb\x00{\x00\x00\x01\xadIDATx^\x95\x93\xd7\xae\xdb@\x0cD=\xe46\xf5.\xd7^no\xe9\xfd\xff\x7f+\xcb\xc0\x16\xd6y\x88\x91\x91\xb0\x101\x87"!\x8cF\xea\x8a\xfe\r\x14\xc5\x15\xe0S~\t\x10\x91\xd2r\x9c\xb5\xabB\x80\xaa\xc5\xc4-\x97\xb7\xaf\xc5\xe5\x0e\x83\x9dE\rF\xfe\xb2]<W\xfao\x80V3\x03$I\x02\x9b`\xf4m}\xa7/\x01z\x99\x02\xd6\x13\xd6B\x84h\xa5C\x80VS\xdf\x8d&>fY\xea\'\x81\x11\x95!P\xcd\xbco\xe3\x85"/\xf5\x10Y0\\\x00Pf\x00\xeb*\x92b[\xe8\xcf?\x19h\x1e\xf5\x00T\x11,\xe2\xad\x12\xed\xdc\xfe\x03\x95\x1bX,\x87\x11\xb4h\x12t\x0b\xe9\xd7\x95\xb3\xe8\xdeQn\x18?\xde\x0f\xc0$I\x10\xab?\xfe\x93\x050\xeew\x1b\xe0{Ng\xe0\t\t\xde\xa4\x92~F3Q\xda\x81qs\x06\xd4\x12\x89\xcd\xe8\xec\xd7\x13\xad\xe8\xc8@{\x06\xf4=X\x80\x9d\xf8\xcc\xa6U\x9a\xde \x80>\x8d\xf8\x05FJ[g\x99\xc1\x80i+ZCF\xd0\txeF\xa4\x8a=\x18\xa6\x96#-\xa7@\xfd0,Yt`_f\x9d\xdf/\x15\xa2>\x18\xc6\xb8\xd7C\xe4\xe2\x11\xf0\xb1\xa4l\xec\xf7K\r\x18r\xbb\xe0S\xcfk\x80g%\xf5\x92\x03y\x073\xf6/\x14\xe4\xc1I\xcb&\xdf\x12iU\x1e\xa4@\xfc\x1c\xe4A\x97\x11\x98a6\xee\x98\xae\xa7\x86\xbdP\x7fy\x0e\x03\xb3\x8a\x18\x8c\x93\xe4\xc1\xe3\x19\x85\x91+o%\'\x0ci\xc6>\xae\x19\x87>\x04\x94V\x8f\xf7_\x8d\xb4\xd6cWTi-~\x00x\x91\xea\xe77m{3\xbf\x93*\x17?\x04Dt\x92\x14\x14\x866\x94\xbe\xfa\xf3\xfe/\xf0\x1b:\xb7\x1f\xde\xf9+;+\x00\x00\x00\x00IEND\xaeB`\x82'
--------html_content---------

>>>>>>>>>>>>>>>>>>>>
request_lines: ['GET /images/trolltech-logo.png HTTP/1.1', 'Host: 127.0.0.1:7892', 'Connection: keep-alive', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 'Accept: image/webp,image/apng,image/*,*/*;q=0.8', 'Referer: http://127.0.0.1:7892/', 'Accept-Encoding: gzip, deflate, br', 'Accept-Language: zh-CN,zh;q=0.9', 'Cookie: csrftoken=XeNEgFEg7BlsE8hp9SKGbVXs0I4j5PY2N10rupEv3B5jMLpQFVs8f4MwCSmXX0mq; sessionid=5bp4uzk26v87sugzrg7jhup8bhxuyj4c', '']
ret: <_sre.SRE_Match object; span=(0, 30), match='GET /images/trolltech-logo.png'>
************************************************** /images/trolltech-logo.png
--------html_content---------
html_content = f.read(): b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xcb\x00\x00\x00 \x08\x03\x00\x00\x00\x8b\xa6|@\x00\x00\x00oPLTE\xa5\xcd8\xfe\xfe\xfe\xa4\xa6\xa9\xb5\xb7\xb9\xd7\xd7\xd9\xef\xf0\xf0\x9e\xa0\xa3\xe6\xe6\xe7\xbd\xbf\xc1\xbf\xc0\xc2\xc5\xc6\xc8\xce\xcf\xd0\xcf\xd0\xd2\x9c\x9e\xa1\xde\xdf\xe0\x9a\x9c\x9f\xef\xef\xf0\xad\xaf\xb1\xf5\xf9\xe9\xaf\xb0\xb3\xac\xd1G\xd9\xea\xab\xe6\xf1\xc8\xde\xec\xb5\xe0\xee\xbc\xca\xe2\x8a\xb4\xd5Y\xff\xff\xff\xbb\xd9h\xec\xf5\xd6\xa9\xcf@\xe3\xef\xc2\xbf\xdbq\xc4\xde}\xf0\xf6\xde\xce\xe4\x92\xd3\xe6\x9dV\xbc3\xac\x00\x00\x054IDATx^\xddX\xd7v\xe3:\x0c\x14X\xd5\xbb{z\xf6\xff\xbf\xf1\x02\xac\x92)\xdf\xe8$/9\x19\xd9Z\x92\xa2\x80\x9d3\x00\x01\'\xbb}\x0f\xa7,\x9b\x9fo\xbf\x0b\xdf\xe5r@.\x1f\x7f\x84\xcb\xe9\xe5/\xe9\xf2\xfb\xb8\xfc\xfa|\x01\x84\xc4\xef\x1e.m\xab\xf1j\xb5v\x03\xba\xc3\rtX\xd7rm\x08\x8eG\x08\xba\xc0y\x0c\x0f\xedK\xeb\xbd=\xae\xc8\xf0\x98\xcc[\x1f\xce\x91y(q\x10\xd7\xb5\\\xf2\x90m]\xe4<\xe7e\xad%\xa4.\xc8\x81n%\xed\xec%d\x8c1\xa5\xf0\xeb\xee\x88\x86#\x97<\xae\x0c\\D60\x1e\xe6\xa71\xe8r\x9c\xaf\xe7\xf0L2\x84^q)\xd1B\xed\'\xb9b\x04\xeb\xcd\xfa\xa5\xed\xc2\xfa\xf5K"R\xd1\xe5\xa0\x1a\x076T\x80K\x93b\x83N\x1d\xc8\xba\xac\xea\xac\xe9\xf0\x8a\xa0\xe9$o\xc0\xdd\xc4\x80\x15\x12<\x95\xf7,\xcb\x0e\xe0t\x01\x9c\xbd\x1cFo\x98\xe1\xd6~\xcd\x05mT~\xc2\xbb\xae\x89\xeeh\xd2\xb0\x16\xb9(\xe7\xd7.y. +\x16\x98\xd0vn\xb8t+\x17P\xa2\x19t\xa0\x91\x8b\xc8\xd8\x80\x17\x02\r*f\x91\x83\xe5\xc2\xf8\xc4\xa7\x895\xf8\xa8p\\\x0c\x959p\x19/\x19\x91q\x0f\xe5\x80\\\xf4=\x97&p)\x18\x82\xbc\xa9\xe0j ]\x1a\xe7z0\xdf\xd6\x8b\xc2\r\x13\xc6\x8b\xb2,8\n$\x0c\x97\xe6\x9e\x8bq\xd0\x8a\xb2j3\x89\x00\t-\xa3Mf(%\xc5\x18Nk\xa0\xb9\x98\xc8\x97\xd5\x15>\x91\xca\xf55\xe4\x0bE\x1c\x0e\\\x98I\xa6\x12]\xba\x05\x170\xf6\xa4\xe4h\xaf\xb6\x8eHo\x81\xaeyOS\xfbuT\xa6F)\xc5E\x0f\x04J\x1cI.\x88\x8b^; \xe1e)\xea\xd2\xd7\x17M\\ \xee!\x7f\xc2Y\x1d\x90Le\x9e\xbd\xceH\xe5\x19\x16\xb5\x12N\xb44\xc6\x18\xd3\x0f\xb9\xa4\xb6\t6\xc68\xdc\xed\x91&0*\x19\xd7\x01\x87\xa9.\x85\rb\x90\xa2\x95\x9eK\x8f\\\x06\x99\xf8s\x81\xa2\xac\xb3\xf1\r\xa9\x1c\xd7\xf5\x05p\x94\xfd3.\xe5V\xbe\xec\xe0\x82{r4\x90\xbc\xc8Dr\x12K\x1etI\x1d\xactYs\t\'J\xed\x9d\x9d_\xec\x7f;\xd6\x17Op|\x90/\xc5\x03.\xcd\x8a\x8bj\xf2\xe8:\x86I\x95P\xd9\xca\x97x\xb8$\xba\xa4\xfe\xa0\xc2q\t8\xb8P8%u\xff\x8c\xc2\x9cl\x8c\xa9]\xba\xe4w\xba\xb0FqHe\xe1\xf2\x96@N{u\x81-\x7f \'7\x1e\x9f\xb2\xec\x02\x8e\x8b\xeb\xc7\xc2\xb2\x8f1\xbd+\xc6\xd8*_\x92\x18\xb3.\xddZ\xaaK\xe2 \xd5\x85m\xe4\x0b@\xcf\x1b\x97\x9b\x1f3\t`q\x8a}2\xc9\xf5\x06>\xc6\xfa]\xb9\xdf\xdcs1g\x1a\x98\x9b\x0f1\xb2\x94\xe6K\xd7\xb1\xd6\x9e\x87@7\xca\xfdT\x974\xf7\x0b\x81(\xa8\xf2L=y8\xce\xa4E\x88\xb1\x17?\xfe\x97eO\xe3\x0f\xce1J\xf3\t\xc1\xe9S\x02-\xc5\x10Ks_\x85RD\x9f-]\x923\x19\xa1l\xb5beoO\xe4E\x9f\xff|\xb9|\x8e\x9e\x97\xe3"\xd9>]\xd2|\xb1\xe8\x08&\x02*\x1b\n\x9b1\x86P\x8bn\x00\xbf_\x9dcy|chI\xf7;]\x80\x90rI\xf3eW}Q\x8a9\xa8\xc2p\xe9\xfe\x8f\x0b[\x02y\xed8\xc7\x14/\x0bN\x1ar\x8a\\\x97/\xe7\r\xfb\x17\xe4b\xf3\xe5\xdb\xf5e\xa2&Y\xd0M;]\x98\xe7\x92\xd6\x17\xa1\xfbp\xe5\xfb\xea\x8b\x12\x00 \x98=\x90\t\xe35\x9ec\x11\xf1\x1c\x03\xb6;\xf7\xd5v}\x89K1{\xd3\xfa\xa2\xbf>\xc7\xd4}\x8c\t_\\\x98\x8e\x02\x8c\x89\xfd#V\xd0\xc3-\x89\xb1\x9f\xd4\x17\xcd:\xb2\x94B\xee<\x93U\xda\x8f\xd9\xc0Q\xaa\x08\xc5\x9e\xfa\xfd5\xe0\xddWP\x18\xf6\xeb\xf2E}\x19\\4|\xbb\x87I\xfb1\'\x8cb\xad\x8b&\xdfZF\x00\x12\xa4\x10\xfbQ\xee7[u\x9f\xf5\xb0\xabVn\xf70I\x8c9Y\xbd/\xa0v\xe5m\x8c.h\xe9J\xfcp\x94\xe4\xfe\xee\xba\xbfq\x00kf\xfaY\xd8\xd5\x8f\xed\xca};\x14\xca\xfb\xb6\xbf\xbd\x9e\x16\xca\xc0y\x8eq\x07l_oIg\xcf:_\x96\xb9\x1f{sU\xacZ~\xd8\x1bc\xfd\xf6\xef\x97(\x8cq\x06\x14e\xd9\xf50\x1a\xc3\x00\x1f\x17\xa2\xf2\t\xb7\xf8[LC\x84s\x05\x11\xd6v\xb7\x11c\xebM\xd0\x9b\xa2\xc8[\xf7\nH\xc1k\xd8\xd9\x8f\xe9\x071\x16\x85\xb1F?\x88Lv\xbd\x9c^\x9f_\x0f\xef\xc4d\xbeP\xe2\x87|\xc9KB\x81W\r6\xf7\'\x9c\xdb\xb5\xb2\x7f\x94/C\x19PI\xff\x0b\x90\xa4\xe1\x95hu[\x17\x83j&\xb9\xdd\'w\xfbz\xcbX\xa0\xc8\x92U\xe6\xfd%#\xcc\xb3\xfb\xf7\x00\x10\xb8\xa00\x11\x93$.\xae\xd3\xe8\xe8\xae\xda\x07\\\x08fO\xac+\xa093s\xe6\xad2\xf1 \xc6\xeaD\x97\xcd\x18\x8b\xc2\xa8\n\xec\x04\xceOY\xc0\xfcN\xc9\x13uY\x82;.\x11Lo\xe6\x8bj"b\xd6\x82\xac\x07e8"\x94b\xfc\xc1\xdf.R.\x92\xf3)\x97\x8b=\x13\xe7\xad\x9f\xc9\x82OS\xe1\x99\xc2x\xc64\xb1\xa1v\x04X\x16\x0e4B\x97\xb9q|\x01jN3\xbb\x82\x1f\x9d\xd8F\xb4a\x8f\xdd\x14,B_q\xc7\x93\x15B\xd2:\x14\xb8E.\\\xd6hY\x04.\x7f\x07\xff\x01\x986\xed\x80\x16\xf12<\x00\x00\x00\x00IEND\xaeB`\x82'
--------html_content---------

				"""

                f.close()
                # 2.1 准备发送给浏览器的数据---header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"
                # 2.2 准备发送给浏览器的数据---boy
                # response += "hahahhah"

                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)

        else:
            # 2.2 如果是以.py结尾，那么就认为是动态资源的请求
            env = dict()
            body = mini_frame.application(env, self.set_response_header)    # return值

            header = "HTTP/1.1 %s\r\n" % self.status

            for temp in self.headers:
                header += "%s:%s\r\n" % (temp[0], temp[1])

            header += "\r\n"

            response = header+body
            # print('################')
            # print('response>>>:', '\n', response)
            # # response打印结果：
            # """
            # response>>>:
            #  HTTP/1.1 200 OK
            # server:mini_web v8.8
            # Content-Type:text/html;charset=utf-8
            #
            # Hello World! 我爱你中国....
            # """
            # print('################')
            # print('header>>>:', '\n', header)
            # # header打印结果：
            # """
            # header>>>:
            #  HTTP/1.1 200 OK
            # server:mini_web v8.8
            # Content-Type:text/html;charset=utf-8
            #
            # """
            # print('################')
            # print('body>>>:', '\n', body)
            # # body打印结果：
            # """
            # body>>>:
            #  Hello World! 我爱你中国....
            # """

            # 发送response给浏览器
            new_socket.send(response.encode("utf-8"))


        # 关闭套接
        new_socket.close()

    def set_response_header(self, status, headers):
        self.status = status
        self.headers = [("server", "mini_web v8.8")]
        self.headers += headers
        

    def run_forever(self):
        """用来完成整体的控制"""

        while True:
            # 4. 等待新客户端的链接
            new_socket, client_addr = self.tcp_server_socket.accept()
            print('self.tcp_server_socket.accept():',self.tcp_server_socket.accept(), 'new_socket:',new_socket,  'client_addr:', client_addr)
            # 打印结果：
            # self.tcp_server_socket.accept():
            # (<socket.socket fd=564, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7892), raddr=('127.0.0.1', 6985)>, ('127.0.0.1', 6985))
            # new_socket:
            # <socket.socket fd=492, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 7892), raddr=('127.0.0.1', 6984)>
            # client_addr: ('127.0.0.1', 6984)
            # 5. 为这个客户端服务
            # 实例化一个进程
            p = multiprocessing.Process(target=self.service_client, args=(new_socket,))
            p.start() # 开启进行

            new_socket.close()


        # 关闭监听套接字
        self.tcp_server_socket.close()


def main():
    """控制整体，创建一个web 服务器对象，然后调用这个对象的run_forever方法运行"""
    wsgi_server = WSGIServer() # 实例一个类对象
    wsgi_server.run_forever()  # 调用类函数


if __name__ == "__main__":
    main()


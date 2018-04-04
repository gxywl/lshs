#!/usr/bin/env python
import os
import unittest

from flask import url_for, request, redirect
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import current_user
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db

from app.models import User, Xiangmu, Bujuan

app=create_app(os.getenv('LSHS_CONFIG') or 'default')

manager = Manager(app)
migrate=Migrate(app,db)


#----------------------

babel = Babel(app)

app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

# ----------------------
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isadm

    #跳转
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class UserView(MyModelView):
#    can_edit = False
#    can_delete = False
#    can_create = False
#    page_size = 5

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        user=u'用户',     username=u'用户名',
    )
#     #column_list = ('Email', 'Username')
#     # column_labels = {
#     #     'Email':u'邮件地址',
#     #     'Username':u'用户名',
#     # }

#     #如果不想显示某些字段，可以重载这个变量
#     column_exclude_list = (
#         'password_hash',
#     )
#
#     column_list = (
#         'username','email',
#     )
#
#
    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class MyAdminIndexView(AdminIndexView):
    #增加这个必须要登录后才能访问，不然显示403错误
    def is_accessible(self):
        return current_user.is_authenticated and current_user.isadm

    #跳转
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    #后台首页
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    # @expose('/user')
    # def user(self):
    #     return self.render('admin/user.html')
    #
    # @expose('/xiangmu')
    # def xiangmu(self):
    #     return self.render('admin/xiangmu.html')
    #
    # @expose('/bujuan')
    # def bujuan(self):
    #     return self.render('admin/bujuan.html')

# admin = Admin(app, name='后台页', template_mode='bootstrap3',index_view=AdminIndexView(name='导航栏',template='admin/welcome.html')) #,url='/admin'
admin = Admin(app, name='数据管理', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative views here
admin.add_view(UserView(db.session, name='用户'))
# admin.add_view(ModelView(Post, db.session, category='Models'))

models = [Xiangmu,Bujuan]
for model in models:
    admin.add_view(MyModelView(model, db.session, category='Models'))

# ----------------------


def make_shell_context():
    return dict(db=db, User=User, Xiangmu=Xiangmu, Bujuan=Bujuan)

manager.add_command('shell', Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests"""
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()

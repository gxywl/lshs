from flask import redirect, url_for, render_template, flash
from flask_login import current_user, login_required
from sqlalchemy import func, engine

from app.models import User, Bujuan, Xiangmu
from .. import db
from .forms import NameForm
from . import main


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = NameForm()
    # bujuan=None
    bujuans = Bujuan.query.filter_by(user=current_user._get_current_object()).order_by(Bujuan.outtime.desc())

    user = current_user._get_current_object()
    if form.validate_on_submit():
        xiangmu = Xiangmu.query.get(form.xiangmu.data)

        bujuan = Bujuan(user=user, xiangmu=xiangmu, jine=form.jine.data)
        db.session.add(bujuan)
        flash('捐出成功')
        return redirect(url_for('.index'))

    # 管理账号转到管理页
    if user.isadm:
        return redirect(url_for('main.count'))
    else:
        # 一般用户转转到首页..
        return render_template('index.html', form=form, bujuans=bujuans)


#
# @main.route('/list')
# def list():
#     bujuans=Bujuan.query.order_by(Bujuan.outtime.desc())
#     return render_template('list.html', bujuans=bujuans)

# @main.route('/user/<username>')
# def user(username):

@main.route('/count')
@login_required
def count():

    countbujuans = db.session.query(Xiangmu.xiangmu, db.func.sum(Bujuan.jine),Xiangmu.id).join(Bujuan).group_by(
        Xiangmu.xiangmu).all()


    alls = db.session.query(db.func.sum(Bujuan.jine)).all()


    countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
        Xiangmu.xiangmu, Bujuan.user).all()

    return render_template('count.html', bujuans=countbujuans, alls=alls,countbujuanbyusers=countbujuanbyusers)

@main.route('/countlist/<int:xiangmuid>')
@login_required
def countlist(xiangmuid):

    alls = db.session.query(db.func.sum(Bujuan.jine)).all()


    countbujuanbyusers = db.session.query(Xiangmu.xiangmu, User.username,db.func.sum(Bujuan.jine)).join(Bujuan).join(User).group_by(
        Xiangmu.xiangmu, User.id).having(Bujuan.xiangmu_id==xiangmuid).all()

    return render_template('countlist.html', alls=alls,countbujuanbyusers=countbujuanbyusers)
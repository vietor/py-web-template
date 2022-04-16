# coding=utf-8

import argparse

from texts import T
from core.db import SessionContext, Session
from core.models import (
    MyUserModel
)


def _get_user(username: str, session: Session) -> MyUserModel:
    user = session.query(MyUserModel).filter_by(username=args.username).first()
    if not user:
        raise Exception(T("user.not_found"))

    return user


def show_user(args, session: Session):
    user = _get_user(args.username, session)
    print(user.to_json())


def add_user(args, session: Session):
    user = session.query(MyUserModel).filter_by(username=args.username).first()
    if user:
        raise Exception(T("user.already_exists"))

    user = MyUserModel(
        username=args.username,
        password=MyUserModel.hash_password(args.password),
        display_name=args.username,
    )
    session.add(user)
    session.commit()
    print(user.to_json())


def passwd_user(args, session: Session):
    user = _get_user(args.username, session)
    user.password = MyUserModel.hash_password(args.password)
    session.add(user)
    session.commit()
    print(user.to_json())


def block_user(args, session: Session):
    user = _get_user(args.username, session)
    user.status = 0 if args.switch == 'on' else -1
    session.add(user)
    session.commit()
    print(user.to_json())


command_table = {
    'show': show_user,
    'add': add_user,
    'passwd': passwd_user,
    'block': block_user
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='User Manage Tools')
    subparsers = parser.add_subparsers(dest="cmd", title="Sub Commands", required=True)

    cmd_show = subparsers.add_parser("show", help="Show User")
    cmd_show.add_argument('username', type=str)

    cmd_add = subparsers.add_parser("add", help="Add User")
    cmd_add.add_argument('username', type=str)
    cmd_add.add_argument('password', type=str)

    cmd_passwd = subparsers.add_parser("passwd", help="Modify Password")
    cmd_passwd.add_argument('username', type=str)
    cmd_passwd.add_argument('password', type=str)

    cmd_block = subparsers.add_parser("block", help="Block or Unblock User")
    cmd_block.add_argument('username', type=str)
    cmd_block.add_argument('switch', type=str, choices=("on", "off"))

    args = parser.parse_args()
    if 'username' in args:
        args.username = args.username.lower()

    with SessionContext() as session:
        try:
            command_table[args.cmd](args, session)
        except Exception as e:
            print('Error:', str(e))

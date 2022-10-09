#  Copyright (c) 2022 Vladyslav Synytsyn.
from typing import Callable

from data.connection.connection_handler import ConnectionHandler
from sqlalchemy.orm import Session


class TransactionManager: ...


# def __init__(self, session):
#     self.__session = session
#
# def __enter__(self):
#     self.__session.begin()
#
# def __exit__(self, exc_type, exc_val, exc_tb):
#     if exc_type is None:
#         self.__session.commit()
#     else:
#         self.__session.rollback()

def transactional(method: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if 'session' in kwargs:
            current_session = kwargs.get('session', None)
            session_provided = True
        elif any((isinstance(arg, Session) for arg in args)):
            current_session = [arg for arg in args if isinstance(arg, Session)][0]
            session_provided = True
        else:
            current_session = ConnectionHandler().create_new_session()
            session_provided = False
        with current_session.begin(nested=True):
            try:
                if session_provided:
                    result = method(*args, **kwargs)
                    current_session.commit()
                else:
                    result = method(*args, **kwargs, session=current_session)
                return result
            except Exception as e:
                current_session.rollback()
                raise e

    return wrapper

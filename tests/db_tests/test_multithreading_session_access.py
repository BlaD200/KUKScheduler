#  Copyright (c) 2022-2022 Vladyslav Synytsyn.

import threading
import unittest
from multiprocessing.pool import ThreadPool
from typing import Callable

from data.connection.connection_handler import ConnectionHandler


class MultiThreadingSessionAccessTest(unittest.TestCase):

    def test_get_current_session_is_thread_safe(self):
        thread_session, session_in_threads = \
            self._emulate_multithreading_access(self.thread_worker_for_get_current_session)
        # print(f'{thread_session=}\n{session_in_threads=}')

        for thread_id, sessions in thread_session.items():
            self.assertEqual(
                len(set(sessions)), 1,
                f'All sessions in one thread must be the same, {thread_id=}, {sessions=}'
            )

        for session_id, threads in session_in_threads.items():
            self.assertEqual(
                len(set(threads)), 1,
                f'Each session shall to be used only in one thread, {session_id=}, {threads=}'
            )

    def test_create_session_creates_new_session_each_time(self):
        thread_session, session_in_threads = \
            self._emulate_multithreading_access(self.thread_worker_for_create_session)
        # print(f'{thread_session=}\n{session_in_threads=}')

        for thread_id, sessions in thread_session.items():
            # All sessions in one thread must be different
            self.assertEqual(
                len(set(sessions)), len(sessions),
                f'All sessions in one thread must be different, {thread_id=}, {sessions=}'
            )

        for session_id, threads in session_in_threads.items():
            self.assertEqual(
                len(threads), 1,
                f'Each session shall to be used only in one thread, {session_id=}, {threads=}'
            )

    @staticmethod
    def thread_worker_for_get_current_session():
        session = ConnectionHandler().get_current_session()
        session.close()
        return {"thread_ident": threading.current_thread().ident, "session_hash": session.hash_key}

    @staticmethod
    def thread_worker_for_create_session():
        session = ConnectionHandler().create_new_session()
        session.close()
        return {"thread_ident": threading.current_thread().ident, "session_hash": session.hash_key}

    @staticmethod
    def update_list_in_dict(dictionary, key, value):
        if key in dictionary:
            dictionary[key].append(value)
        else:
            dictionary[key] = [value]

    def _emulate_multithreading_access(self, func: Callable):
        thread_session = {}
        session_in_threads = {}
        with ThreadPool(8) as pool:
            for i in range(1, 100):
                print(f'{threading.current_thread().name} is starting evaluate {i}')
                res = pool.apply_async(func).get()

                self.update_list_in_dict(thread_session, res["thread_ident"], res["session_hash"])
                self.update_list_in_dict(session_in_threads, res["session_hash"], res["thread_ident"])
        return thread_session, session_in_threads

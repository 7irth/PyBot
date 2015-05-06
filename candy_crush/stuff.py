__author__ = 'Tirth'

import requests as req
import json

session = 'CwAFwreJgqrBfZ4VtCF46Q.1'
user_id = '1481041553'


def start_game(sesh, episode, level):
    params = {"_session": sesh, "arg0": episode, "arg1": level}
    response = req.get("http://candycrush.king.com/api/gameStart",
                            params=params)
    return response.json()


def add_life():
    params = {"_session": session}
    print(req.get("http://candycrush.king.com/api/addLife", params=params))


if __name__ == '__main__':
    print(start_game(session, 1, 1))
    add_life()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from sys import argv

from asyncio import get_event_loop
from aiohttp import ClientSession, WSMsgType


async def follow(filename):
    url = 'http://localhost:9292/follow/{}'.format(filename)

    async with ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    print('{} :: {}'.format(filename, msg.data), end='')
                elif msg.type == WSMsgType.CLOSED:
                    print('CLOSED!')
                    break
                elif msg.type == WSMsgType.ERROR:
                    print('ERROR!')
                    break


loop = get_event_loop()
loop.run_until_complete(follow(argv[1]))

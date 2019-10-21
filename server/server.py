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

from pathlib import Path
from contextlib import closing
from asyncio import get_event_loop

from aiohttp import web
from aionotify import Watcher, Flags
from aiofile import AIOFile, LineReader


async def handle(request):

    # Check file exists
    rawfn = request.match_info.get('filename', None)

    if not rawfn:
        raise web.HTTPBadRequest(
            reason='Filename must be specified'
        )

    cleanfn = Path(rawfn).name
    fnpath = Path().cwd() / cleanfn

    if not fnpath.is_file():
        raise web.HTTPNotFound(reason='File {} not found'.format(rawfn))

    # Send websocket response
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Create watcher for file
    with closing(Watcher()) as watcher:
        watcher.watch(path=str(fnpath), flags=Flags.MODIFY)

        await watcher.setup(get_event_loop())
        print('Watcher created for "{}"'.format(fnpath))

        async with AIOFile(fnpath, mode='r', encoding='utf-8') as afd:
            print('Sending lines!')
            reader = LineReader(afd)

            async for line in reader:
                print(line, end='')
                await ws.send_str(line)

            while True:
                event = await watcher.get_event()
                print('Got event! {}'.format(event))
                async for line in reader:
                    print(line, end='')
                    await ws.send_str(line)

    return ws


app = web.Application()
app.add_routes([
    web.get('/follow/{filename}', handle),
])


if __name__ == '__main__':
    web.run_app(app, port=9292)

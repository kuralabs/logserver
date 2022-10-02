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
from aiohttp import web
from sh import tail

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

    

    for line in tail("-f", fnpath, _iter=True):
        await ws.send_str(line)

    return ws


app = web.Application()
app.add_routes([
    web.get('/follow/{filename}', handle),
])


if __name__ == '__main__':
    web.run_app(app, port=9292)

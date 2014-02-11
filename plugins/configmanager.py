import plugins as plugin
from core.protocol import config

@registerCommand('cfg',0,requires_admin=True,min_args=2,max_args=3)
def cfgMgr(proto,user,channel,args):
	

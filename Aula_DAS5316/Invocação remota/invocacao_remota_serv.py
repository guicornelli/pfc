from xmlrpc.server import SimpleXMLRPCServer
#  RPC - Remote Procedure Call
#  Utiliza XML para fazer o encode e HTTP como mecanismo de transporte
from xmlrpc.server import SimpleXMLRPCRequestHandler
#  Manipulador de Requests/Pedidos


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
#  Classe para tratar o request do cliente


with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:

    def adder_function(x, y):
        return x + y


    def mult_function(x, y):
        return x*y


    def exp_function(x, y):
        return x**y


    def sub_function(x, y):
        return x - y


    server.register_function(adder_function, 'add')
    server.register_function(mult_function, 'mult')
    server.register_function(exp_function, 'exp')
    server.register_function(sub_function, 'sub')
    server.serve_forever()

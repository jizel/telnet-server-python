import SocketServer
import threading
import sys
from commands.commands import Commands
from parse_args import get_complete_args


class MyHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for my server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    # Reg expressions from command line args
    re_dict_args= {}
    #default value for max concurrent connections, can be changed by params
    max_users = 5
    # File with reg expressions from cmd args
    reg_file = ""

    def handle(self):
        # Check max users limit when client tries to connect
        no_of_active_users = threading.active_count() -1
        thread_number = threading.currentThread().getName()[-1:]
        if no_of_active_users <= int(self.max_users):
            self.request.sendall("Welcome client %s\n\r" % thread_number)
        else:
            self.request.sendall("No slots available now. Try to connect later. \n\r")
            data = self.request.recv(1024)
            return False

        # Commands initialization for each client
        cmds = Commands()
        cmds_dict = cmds.comm_dict
        cmds.reg_dict.update(self.re_dict_args)
        cmds.client = threading.currentThread().getName()
        cmds.active_re_on[cmds.client] = False
        if self.reg_file:
            cmds.reg_file = self.reg_file

        # Read client's input and parse commands
        while True:
            # self.request is the TCP socket connected to the client
            data = self.request.recv(1024).strip()
            # quit - if it looks stupid but it works it ain't stupid?
            if data == "quit":
                self.request.sendall("Do you really want to shutdown the server (yes/no)?\n")
                resp = self.request.recv(1024).strip()
                if resp == "yes":
                    myServer.shutdown()
                    break

            # Uncomment for debugging
            # cur_thread = threading.currentThread().getName()
            # print "{} wrote:".format(cur_thread)
            # print data

            result = self.parse(data, cmds_dict)
            if result:
                self.request.sendall(result)
                self.request.sendall("\n")
            else:
                if data:
                    # Repeat non-parsed input to client
                    self.request.sendall(data)
                    self.request.sendall("\n")
                # else:
                #     # In case of closing the client terminal window to prevent except
		        #     # Seems to be an issue in pycharm only -> commented
                #     break

    # The parsing function, d is the command dictionary
    def parse(self, user_input, d):
        parse_input = user_input.split(" ")
        function = parse_input[0]
        args = parse_input[1:]
        if function == "help" and args:
            return d[args[0]].__doc__
        elif function in d:
            try:
                return d[function](*args)
            except TypeError:
                return "Wrong number of arguments. Type help [function_name] for help"
        else:
            return False


class MyThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    Overrides TCPServer and enables threads by using ThreadingMixIn
    """
    allow_reuse_address = True
    # Allow daemon_threads in case you want to shutdown server immediately (close all connections) with "quit"
    daemon_threads = True


# Initialize the server - not very nice to have it here but needed for shutdown
args = get_complete_args()

if ('host' in args) and ('port' in args):
    HOST = args['host']
    PORT = int(args['port'])
else:
    print "\n Host and port not specfied! Use command line args -H -p or configuration file.\n"
    sys.exit(1)

if 'maxuser' in args:
    MyHandler.max_users = args['maxuser']

if 'reg_file' in args:
    MyHandler.reg_file = args['reg_file']

if 'reg_exp' in args:
    for reg in args['reg_exp']:
        # Add each reg exp argument from command line or file with it's index as name
        MyHandler.re_dict_args[str(args['reg_exp'].index(reg))] = reg


myServer = MyThreadedServer((HOST, PORT), MyHandler)


def run_server():
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        myServer.shutdown()
        sys.exit(0)




# Not used!!!


# class MyServer:
#     def __init__(self,host,port):
#         # Initialize server and create an instance
#         self.myServer = MyThreadedServer((host, port), MyHandler)
#
#     def run_server(self):
#         try:
#             self.myServer.serve_forever()
#         except KeyboardInterrupt:
#             self.server.shutdown()
#             sys.exit(0)
#
#     def stop_server(self):
#         self.myServer.shutdown()
#
#     def get_server(self):
#         return self.myServer

# Client:
# t = threading.Thread(target=server.serve_forever)
# t.setDaemon(True) # don't hang on exit
# t.start()
# print 'Server loop running in thread:', t.getName()

#  # Connect to the server
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s2.connect((HOST, PORT))
#
# # Send the data
# message = 'Hello, world'
# print 'Sending : "%s"' % message
# len_sent = s.send(message)
# s2.send('blblbbl')
#
# # Receive a response
# response = s.recv(1024)
# print 'Received: "%s"' % response
# resp2 = s2.recv(1024)
# print 'Response 2: "%s"' % resp2
#
# # Clean up
# s.close()
# s2.close()
# server.socket.close()

from server import run_server

def main():

    run_server()

    # Not used now - moved to server
    # args = get_complete_args()
    # for reg in args['reg_exp']:
    #     MyHandler.cmds.reg_dict[str( args['reg_exp'].index(reg))] = reg
    #
    # if ('host' in args) and ('port' in args):
    #     HOST = args['host']
    #     PORT = int(args['port'])
    #     # Initialize server and create an instance
    #     # myServer = MyThreadedServer((HOST, PORT), MyHandler)
    #     server.HOST = HOST
    #     server.PORT = PORT
    #
    #     if 'maxuser' in args:
    #         MyHandler.max_users = args['maxuser']
    #
    #     for reg in args['reg_exp']:
    #         MyHandler.cmds.reg_dict[str( args['reg_exp'].index(reg))] = reg
    #     server.run_server()
    # else:
    #     print "\n Specify host and port first! \n"
    #     pass


if __name__ == "__main__":
    main()




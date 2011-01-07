from tornado import Server

# Import your module here
# e.g. import mymodule


if __name__ == "__main__":
    server = Server()
    # Register your urls here
    # e.g. server.register("/foo", mymodule.foohandler)

    server.run()

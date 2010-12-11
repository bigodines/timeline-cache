from server import Timeline, TimelineFactory
from twisted.internet import reactor

if __name__ == "__main__":
	reactor.listenTCP(8666, TimelineFactory("hello"))
	reactor.run()

CC=g++
CFLAGS= -Werror -Wall
LIBS= -pthread

customizable_http_server: customizable_http_server.cc flow.cc
	${CC} ${CFLAGS} ${LIBS} $^ -o $@

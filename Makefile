CPPFLAGS = -O2
LDLIBS =

all: utils
clean:
	rm -f utils *.o

utils: utils.o
	$(CXX) $(LDFLAGS) $^ $(LDLIBS) -o $@
utils.o:

.PHONY: all clean distclean run debug memcheck
.DEFAULT_GOAL = all

packages = gtk4 gtk4-layer-shell-0

CC = gcc
CFLAGS = -O2 -g -I include $(shell pkg-config -cflags $(packages)) 

LD = $(CC)
LDFLAGS = $(CFLAGS)
LDLIBS = $(shell pkg-config -libs $(packages))

sources := $(shell find -name "*.c")

%.d: %.c
	$(CC) $(CFLAGS) -MM -MT $(@:.d=.o) $< -MF $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

dshell: $(sources:.c=.o)
	$(LD) $(LDFLAGS) $^ -o $@ $(LDLIBS)

style.css: style/application.scss $(wildcard style/**/*.scss)
	sass --no-source-map $< $@

all: style.css
	bear --append -- $(MAKE) dshell

clean:
	@rm -vf **/*.d **/*.o

distclean: clean
	rm style.css

run: all
	@./dshell

debug: all
	GTK_DEBUG=interactive ./dshell

memcheck: all
	valgrind --leak-check=full ./dshell

ifeq (,$(filter clean,$(MAKECMDGOALS)))
include $(sources:.c=.d)
endif

# Makefile

TGT = RELEASE.txt

all: $(TGT)

$(TGT):
	date -Isec > $@
	git remote -v >> $@
	git describe --long --tags --dirty >> $@

clean clobber nuke:
	-rm $(TGT)

# vim: set sw=8 ts=8 noet ic ai:

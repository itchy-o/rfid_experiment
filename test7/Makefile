# Makefile - for Linux
# build a release

TGT = RELEASE.txt
MPY = assign_xy.mpy tag_coords.mpy test7.mpy

.PHONEY: all
all: $(TGT) $(MPY)

$(TGT): FORCE
	> $@
	git describe --long --tags --dirty >> $@
	git remote -v | awk '/ \(fetch\)$$/ {print $$2}' >> $@
	date -Isec >> $@

%.mpy : %.py
	./mpy-cross-raspios-9.2.1 $<

.PHONEY : clean clobber nuke
clean clobber nuke:
	-rm -f $(TGT) $(MPY)

.PHONEY: FORCE
FORCE:

# vim: set sw=8 ts=8 noet ic ai:

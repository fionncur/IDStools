FC?=ifort
FCFLAGS?=-g
LDFLAGS?=

INSTALL_DIR?=.

IMAS_FCFLAGS?=`pkg-config --cflags imas-$(FC)`
AMNS_FCFLAGS?=`pkg-config --cflags amns`

IMAS_LDFLAGS?=`pkg-config --libs imas-$(FC)`
AMNS_LDFLAGS?=`pkg-config --libs amns`

TARGET=FP_dummy_plasma.exe
DATA=FP_parameters.dat

.PHONY: clean

ALL: ${TARGET}

check:
	echo ${FC}
	echo ${IMAS_FCFLAGS}

install: ${TARGET}
	install -d ${INSTALL_DIR}/bin
	install -d ${INSTALL_DIR}/share
	install ${TARGET} ${INSTALL_DIR}/bin/.
	install ${DATA} ${INSTALL_DIR}/share/.

clean:
	@rm *.o ${TARGET}

FP_dummy_plasma.exe: FP_dummy_plasma.F90
	${FC} ${FCFLAGS} ${IMAS_FCFLAGS} ${AMNS_FCFLAGS} $^ -o $@ ${LDFLAGS} ${IMAS_LDFLAGS} ${AMNS_LDFLAGS}

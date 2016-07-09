
# GFORTRAN
ifndef OBJECTCODE
  OBJECTCODE=gfortran
endif

include ../config/$(OBJECTCODE)
F90FLAGS+= -fPIC
ifdef DEBUG
  F90FLAGS+= -g
else
  F90FLAGS+= -O3
endif

INCLUDE+=$(shell pkg-config --cflags ggd_$(OBJECTCODE))
LIBS+=   $(shell pkg-config --libs ggd_$(OBJECTCODE))

EXE=ex1_writing_structured.exe
RUN=$(addprefix &&./, $(EXE))

all: test

test: progs
	@echo "Run tests:" $(RUN)

progs: $(EXE)

%.exe: %.o
	$(F90) $(F90FLAGS) -o $@ $^ $(LIBS)

%.o: %.f90
	echo $(INCLUDE)
	$(F90) $(F90FLAGS) $(INCLUDE) -c  $< -o $@

clean:
	rm *.o *.mod *.exe


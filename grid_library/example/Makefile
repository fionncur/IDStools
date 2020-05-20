
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

INCLUDE+=$(shell pkg-config --cflags imas_ggd_$(OBJECTCODE))
LIBS+=   $(shell pkg-config --libs imas_ggd_$(OBJECTCODE))

EXE=ex1_writing_structured.exe ids_grid_example1_2dstructured_servicelibrary.exe
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
	rm -f *.o *.mod *.exe
	rm -rf *.exe.dSYM/

veryclean: clean
	rm -f *~

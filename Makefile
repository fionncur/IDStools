VERSION=1.0.0

# ------------------------------------------------
# LINKS TO THE IMAS LIBRARY AND INCLUDE DIRECTORY
# ------------------------------------------------
# INTEL
#OBJECTCODE=intel
#F90=ifort            # FORTRAN COMPILER
#LIBS=`pkg-config imas-ifort imas-lowlevel --libs` `pkg-config imas-ifort --cflags`
#F90FLAGS=-fPIC -fpp # FPIC AND PREPROCESSING OPTION
#MOD_LOCATION_FLAG= -module

# GFORTRAN
ifndef OBJECTCODE
  OBJECTCODE=gfortran
endif

include config/$(OBJECTCODE)

OBJ=$(OBJECTCODE)/obj
LIB=$(OBJECTCODE)/lib
PKG=$(shell pwd)/pkg-config

OBJECTS=$(OBJ)/ids_schemas.o $(OBJ)/ids_grid_access.o $(OBJ)/ids_grid_structured.o

EXE=$(LIB)/prog_ids_grid_structured.exe
RUN=$(addprefix &&, $(EXE))

LIBNAME=$(LIB)/libggd.a

PC_FILES=$(PKG)/ggd_$(OBJECTCODE).pc

all: install test

test: progs
	@echo "Run tests:" $(RUN)

progs: $(EXE)

install: library $(PC_FILES)

library: $(LIBNAME)

$(LIBNAME): $(OBJECTS)
	@make mkdirs
	ar -cvr $@ $^

$(LIB)/%.exe: $(OBJECTS) $(OBJ)/%.o
	@make mkdirs
	$(F90) $(F90FLAGS) -o $@ $^ $(LIBS)

# RULES FOR ALL OBJECT FILES
$(OBJ)/%.o: %.f90
	@make mkdirs
	$(F90) $(MOD_LOCATION_FLAG) $(OBJ) $(F90FLAGS) -c  $< $(INCLUDE) -o $@

mkdirs:
	@mkdir -p $(OBJ) $(LIB) 2> /dev/null

%.pc: trigger
	cat $@.template | sed 's|=GGDVERSION=|$(VERSION)|g' | sed 's|=GGDPATH=|$(PKG)/$(OBJECTCODE)|g' > $@

trigger:

.PHONY: mkdirs clean veryclean \
	library progs test all trigger

# CLEAN DIRECTORY
clean:
	rm -f *.exe $(LIB)/*.a $(OBJ)/*.mod $(OBJ)/*.o

veryclean:
	rm -f *~ */*~
	rm -f */*/*.a */*/*.mod */*/*.o
	-rmdir $(OBJ) $(LIB) $(OBJECTCODE) 2> /dev/null

VERSION=1.0.1

ifndef OBJECTCODE
  OBJECTCODE=gfortran
endif

include config/$(OBJECTCODE)
F90FLAGS+= -fPIC
ifdef DEBUG
  F90FLAGS+= -g
else
  F90FLAGS+= -O3
endif

SRC=src
OBJ=$(OBJECTCODE)/obj
LIB=$(OBJECTCODE)/lib
BIN=$(OBJECTCODE)/bin
PKG=$(shell pwd)/pkg-config

OBJECTS=$(OBJ)/ids_grid_common.o $(OBJ)/ids_grid_access.o $(OBJ)/ids_grid_structured.o

EXE=$(BIN)/prog_ids_grid_structured.exe
RUN=$(addprefix &&, $(EXE))

LIBNAME=$(LIB)/libggd.a

PC_FILES=$(PKG)/ggd_$(OBJECTCODE).pc

all: install test

test: progs
	@echo "Run tests:" $(RUN)

progs: $(EXE)

install: library $(PC_FILES)

install_all:
	make install OBJECTCODE=gfortran
	make install OBJECTCODE=intel

library: $(LIBNAME)

$(LIBNAME): $(OBJECTS)
	@make mkdirs
	ar -cvr $@ $^

$(BIN)/%.exe: $(OBJECTS) $(OBJ)/%.o
	@make mkdirs
	$(F90) $(F90FLAGS) -o $@ $^ $(LIBS)

# RULES FOR ALL OBJECT FILES
$(OBJ)/%.o: $(SRC)/%.f90
	@make mkdirs
	$(F90) $(MOD_LOCATION_FLAG) $(OBJ) $(F90FLAGS) -c  $< $(INCLUDE) -o $@

mkdirs:
	@mkdir -p $(OBJ) $(LIB) $(BIN) 2> /dev/null

%.pc: trigger
	cat $@.template | sed 's|=GGDVERSION=|$(VERSION)|g' | sed 's|=GGDPATH=|$(shell pwd)/$(OBJECTCODE)|g' > $@
	@echo "================================================================="
	@echo "To use new library update your PKG_CONFIG_PATH (assuming bash):"
	@echo "export PKG_CONFIG_PATH=\$$PKG_CONFIG_PATH:$(PKG)"
	@echo "================================================================="

trigger:

get_pkg_path:
	@echo ${PKG}

.PHONY: mkdirs clean veryclean \
	library progs test all trigger

# CLEAN DIRECTORY
clean:
	rm -f $(BIN)/*.exe $(LIB)/*.a $(OBJ)/*.mod $(OBJ)/*.o $(PKG)/*.pc

veryclean: clean
	make clean -C example/
	rm -f *~ */*~
	rm -f */*/*.a */*/*.mod */*/*.o */*.pyc */*.exe
	-rmdir $(OBJ)/ $(LIB)/ $(OBJECTCODE)/ $(BIN)/ 2> /dev/null
	rm -f *~

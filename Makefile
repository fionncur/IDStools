VERSION=1.0.2
CODENAME=imas_ggd

ifndef OBJECTCODE
  OBJECTCODE=gfortran
endif

ifndef INSTALL_DIR
  INSTALL_DIR=${shell echo ${HOME}}/codes/INSTALL/${CODENAME}
endif
INSTALL_DIR_EXTENDED=${INSTALL_DIR}/$(VERSION)/$(OBJECTCODE)

include config/${OBJECTCODE}
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
PKG=pkg-config

OBJECTS=$(OBJ)/ids_grid_common.o $(OBJ)/ids_grid_access.o $(OBJ)/ids_grid_structured.o

EXE=$(BIN)/prog_ids_grid_structured.exe
RUN=$(addprefix &&, $(EXE))

LIBNAME=$(LIB)/lib${CODENAME}.a

PC_FILES=$(PKG)/${CODENAME}_${OBJECTCODE}.pc

all: install test

test: progs
	@echo "Run tests:" $(RUN)

progs: $(EXE)

#install: library $(PC_FILES)

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
	NAME=${shell echo $@ |sed 's/_${OBJECTCODE}//g'}; \
	cat $$NAME.template | sed 's|@GGDVERSION@|$(VERSION)|g' | sed 's|@OBJECTCODE@|$(OBJECTCODE)|g' | sed 's|@GGDPATH@|${INSTALL_DIR_EXTENDED}|g' > $@

trigger:

install: clean library ${PC_FILES}
	@echo "Installing ${CODENAME} at ${INSTALL_DIR_EXTENDED}..."
	mkdir -p ${INSTALL_DIR_EXTENDED}/lib
	mkdir -p ${INSTALL_DIR_EXTENDED}/include
	mkdir -p ${INSTALL_DIR_EXTENDED}/pkg-config
	install ${LIB}/*.a    ${INSTALL_DIR_EXTENDED}/lib
	@#install ${LIB}/*.so   ${INSTALL_DIR_EXTENDED}/lib
	install ${OBJ}/*.mod  ${INSTALL_DIR_EXTENDED}/include
	install ${PKG}/*.pc   ${INSTALL_DIR_EXTENDED}/pkg-config
	@echo "================================================================="
	@echo "To use new library update your PKG_CONFIG_PATH (assuming bash):"
	@echo "export PKG_CONFIG_PATH=\$$PKG_CONFIG_PATH:${INSTALL_DIR_EXTENDED}/pkg-config"
	@echo "================================================================="

.PHONY: mkdirs clean veryclean \
	library progs test all trigger

# CLEAN DIRECTORY
clean:
	rm -f $(BIN)/*.exe $(LIB)/*.a $(OBJ)/*.mod $(OBJ)/*.o $(PKG)/*.pc

veryclean: clean
	make clean -C example/
	rm -f *~ */*~
	rm -f */*/*.a */*/*.mod */*/*.o */*.pyc */*.exe
	rm -rf $(BIN)/*.exe.dSYM/
	-rmdir $(OBJ) $(LIB) $(BIN) $(OBJECTCODE) 2> /dev/null
	rm -f *~

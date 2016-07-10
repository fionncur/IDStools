import xml.etree.ElementTree as ET

input_filename='coordinate_identifier.xml'
output_filename='../src/ids_grid_common.f90'

ROOT=ET.parse(input_filename);

MAX_ROW_LENGTH=124

FILE_STR = """module ids_grid_common

  use iso_c_binding, only: DP => c_double

  implicit none

  integer, parameter :: GRID_UNDEFINED = 0

  ! Data representation definitions
  integer, parameter :: GEO_TYPE_STANDARD = 1
  character(*), parameter :: GEO_TYPE_ID_STANDARD = "Standard"
  integer, parameter :: GEO_TYPE_FOURIER = 2
  character(*), parameter :: GEO_TYPE_ID_FOURIER = "Fourier"

 ! Field aligned vector definitions
  integer, parameter :: VEC_ALIGN_DEFAULT = 1
  character(len=132), parameter :: VEC_ALIGN_DEFAULT_ID = "DEFAULT"

  integer, parameter :: VEC_ALIGN_POLOIDAL = 1001
  character(len=132), parameter :: VEC_ALIGN_POLOIDAL_ID = "Poloidal"
  integer, parameter :: VEC_ALIGN_RADIAL = 1002
  character(len=132), parameter :: VEC_ALIGN_RADIAL_ID = "Radial"
  integer, parameter :: VEC_ALIGN_PARALLEL = 1003
  character(len=132), parameter :: VEC_ALIGN_PARALLEL_ID = "Parallel"

  integer, parameter :: VEC_ALIGN_TOROIDAL = 1004
  character(len=132), parameter :: VEC_ALIGN_TOROIDAL_ID = "Toroidal"

"""

index_list=[]
for ele in ROOT.getroot().findall('int'):
    index = eval(ele.text)
    name = ele.attrib['name']
    description = ele.attrib['description']

    N_rows = len(description)/MAX_ROW_LENGTH
    for j in range( N_rows+1 ):
        if j > 0:
            FILE_STR+='  !> ...'
        else:
            FILE_STR+='  !> '
        FILE_STR+=description[j*MAX_ROW_LENGTH:(j+1)*MAX_ROW_LENGTH-1]
        if j < N_rows:
            FILE_STR+='...'
        FILE_STR+='\n'
    FILE_STR+='  integer, parameter :: COORDTYPE_'+name+' = '+str(index)+'\n\n'

    index_list.append(index)
    
    print 'Coord ', index,' = ', name,'  # ', description

NEW_STR ='  integer, parameter :: LIST_COORDINATES('+str(len(index_list))+')=(/ &\n'
for j in range(len(index_list)):
    s = str( index_list[j] )
    if j==0:
        NEW_STR+='        '+s
    elif len(NEW_STR)+len(s) > MAX_ROW_LENGTH:
        FILE_STR+=NEW_STR+' , &\n'
        NEW_STR='        '+s
    else:
        NEW_STR+=', '+s
FILE_STR+=NEW_STR+' /)\n'

FILE_STR+="""
end module ids_grid_common
"""

f=open(output_filename,'w');
f.write( FILE_STR );
f.close();


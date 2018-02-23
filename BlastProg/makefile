# igraph library
PATH_IGRAPH_LIB = -L/usr/local/lib
PATH_IGRAPH_INC = -I/usr/local/include/igraph

# source files
SOURCESCB = ./cleanBlast/src/*.cpp
SOURCESFD = ./familyDetector/src/*.cpp

# executables name and path def
EXECNAMECB = CleanBlast
EXECNAMEFD = FamilyDetector
EXECPATH = ./

# parameters for g++ compiler
GCC_NAME    = g++
GCC_FLAGS   = -std=c++11
GCC_LIBS    = -ligraph -pthread

.SUFFIXES: .cpp

exec:	$(OBJECTS)
	$(GCC_NAME) $(SOURCESCB) $(GCC_FLAGS) -o $(EXECPATH)$(EXECNAMECB)
	$(GCC_NAME) $(SOURCESFD) $(PATH_IGRAPH_INC) $(PATH_IGRAPH_LIB) $(GCC_LIBS) $(GCC_FLAGS) -o $(EXECPATH)$(EXECNAMEFD)

clean:
	rm $(EXECNAMECB) $(EXECNAMEFD)
# END

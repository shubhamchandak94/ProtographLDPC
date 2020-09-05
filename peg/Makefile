# GCC Makefile for: PEG-ECC by Xiao-Yu Hu.
# http://www.inference.phy.cam.ac.uk/mackay/PEG_ECC.html
#
# Tested with on Linux 2.4 and 2.6 (i686) with
# GCC versions 3.2.2, 3.3.5 and GNU Make version 3.80.
#
# Simeon Miteff <simeon@up.ac.za>
# Thu May 12 12:38:41 SAST 2005

PROGRAM = MainPEG
OBJECTS = MainPEG.o CyclesOfGraph.o BigGirth.o

CXX = g++
CXXFLAGS = -g -ansi -pedantic -Wno-deprecated -Wall -O2 -std=c++11
#CXXFLAGS = -g -ansi -pedantic -Wall -march=native -ftree-vectorize -O3

.SUFFIXES: .o .C

all: ${OBJECTS}
		$(CXX) -o ${PROGRAM} ${OBJECTS}

.C.o: $<
		$(CXX) ${CXXFLAGS} -c $< -o $@

.PHONY : clean

clean:
		rm -f ${OBJECTS} ${PROGRAM} *~ *.log

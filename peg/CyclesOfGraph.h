#ifndef CYCLESOFGRAPH
#define CYCLESOFGRAPH 1

#include <cstdlib>
#include <iostream> // C++ I/O library header
//#include <iomanip.h>

class NodesOfGraph{
 public:
  int numOfParityConnections;
  int *parityConnections;
  int numOfSymbolConnections;
  int *symbolConnections;
  int numOfSymbolMapping;
  int *symbolMapping;
  NodesOfGraph(void);
  ~NodesOfGraph(void);
  void setParityConnections(int num, int *value);
  void setSymbolConnections(int num, int *value);
  void setSymbolMapping(int num, int *values);
}; //Why this is necessary?

class CyclesOfGraph {
 public:
  int M, N;
  int *(*H);
  int *cyclesTable;
  NodesOfGraph *nodesOfGraph;
  CyclesOfGraph(int mm, int n, int *(*h));
  ~CyclesOfGraph(void);
  void getCyclesTable(void);
  void printCyclesTable(void);
  int girth(void);
 private:
  int *tmp, *med, *tmpCycles;
};

#endif



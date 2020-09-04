/************************************************************************/
/*                                                                      */
/*        Free software: Progressive edge-growth (PEG) algorithm        */
/*        Created by Xiaoyu Hu                                          */
/*                   Evangelos Eletheriou                               */
/*                   Dieter Arnold                                      */
/*        IBM Research, Zurich Research Lab., Switzerland               */
/*                                                                      */
/*        The C++ sources files have been compiled using xlC compiler   */
/*        at IBM RS/6000 running AIX. For other compilers and platforms,*/
/*        minor changes might be needed.                                */
/*                                                                      */
/*        Bug reporting to: xhu@zurich.ibm.com                          */
/**********************************************************************/

////
// Modified by F. P. Beekhof; 2008 / 08 / 19
////

#include <cstdlib>
#include <cstring>
#include <string>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <vector>
#include "BigGirth.h"
#include "CyclesOfGraph.h"

const double EPS = 1e-6;

using namespace std;

void usage()
{
    cout<<"*******************************************************************************************"<<endl;
    cout<<" Usage Reminder: MainPEG -numM M -numN N -codeName CodeName -degFileName DegFileName " <<endl;
    cout<<"         option:         -sglConcent SglConcent                                     " <<endl;
    cout<<"                         sglConcent==0 ----- strictly concentrated parity-check      " <<endl;
    cout<<"                                       degree distribution (including regular graphs)" <<endl;
    cout<<"                         sglConcent==1 ----- Best-effort concentrated (DEFAULT)      " <<endl;
    cout<<"         option:         -tgtGirth TgtGirth                                          " <<endl;
    cout<<"                  TgtGirth==4, 6 ...; if very large, then greedy PEG (DEFAULT)       " <<endl;
    cout<<"                  IF sglConcent==0, TgtGirth is recommended to be set relatively small" <<endl;
    cout<<"         option:         -q                                          " <<endl;
    cout<<"                  Quiet mode. Produces less output to the screen .       " <<endl;
    cout<<"         option:         -outputMode <0,1,2>                                    " <<endl;
    cout<<"                  Specifies output format.      " <<endl;
    cout<<"                  '0': H in compressed format (default)       " <<endl;
    cout<<"                  '1': H in un-compressed format       " <<endl;
    cout<<"                  '2': G and H in compressed format       " <<endl;
		cout<<"         option:         -seed SeedVal; unsigned integer, default 0                    " <<endl;
    cout<<"                                                                                       " <<endl;
    cout<<" Remarks: File CodeName stores the generated PEG Tanner graph. The first line contains"<<endl;
    cout<<"          the block length, N. The second line defines the number of parity-checks, M."<<endl;
    cout<<"          The third line defines the number of columns of the compressed parity-check "<<endl;
    cout<<"          matrix. The following M lines are then the compressed parity-check matrix.  "<<endl;
    cout<<"          Each of the M rows contains the indices (1 ... N) of 1's in the compressed  "<<endl;
    cout<<"          row of parity-check matrix. If not all column entries are used, the column  "<<endl;
    cout<<"          is filled up with 0's.                                                      "<<endl;
    cout<<"                                                                                      "<<endl;
    cout<<"          If both G and H are in the output, (outMode 2), the first line contains"<<endl;
    cout<<"          N, the 2nd line K, the number of message bits, the 3rd line M, the 4th line"<<endl;
    cout<<"          contains the number of rows of the compressed generator matrix; the 5th"<<endl;
    cout<<"          defines the number of columns of the compressed parity-check matrix. The"<<endl;
    cout<<"          format of G is almost like that of H, but vertical -- i.e. the padding"<<endl;
    cout<<"          zeroes are on the bottom.   "<<endl;

    cout<<"                                                                                      "<<endl;
    cout<<"          File DegFileName is the input file to specify the degree distribution (node "<<endl;
    cout<<"          perspective). The first line contains the number of various degrees. The second"<<endl;
    cout<<"          defines the row vector of degree sequence in the increasing order. The vector"<<endl;
    cout<<"          of fractions of the corresponding degree is defined in the last line.         "<<endl;
    cout<<"                                                                                       "<<endl;
    cout<<"          A log file called 'leftHandGirth.log' will also be generated and stored in the"<<endl;
    cout<<"          current directory, which gives the girth of the left-hand subgraph of j, where"<<endl;
    cout<<"          1<=j<=N. The left-hand subgraph of j is defined as all the edges emanating from"<<endl;
    cout<<"          bit nodes {1 ... j} and their associated nodes (not created in quiet mode).    "<<endl;
    cout<<"                                                                                         "<<endl;
    cout<<"          The last point is, when strictly concentrated parity-check degree distribution"<<endl;
    cout<<"          is invoked, i.e. sglConcent==0, the girth might be weaken to some extent as    "<<endl;
    cout<<"          compared to the generic PEG algorithm.                                         "<<endl;
    cout<<"**********************************************************************************************"<<endl;
    exit(-1);
}

int main(int argc, char * argv[]){
  int sglConcent=1;  // default to non-strictly concentrated parity-check distribution
  int targetGirth=100000; // default to greedy PEG version
  std::string codeName, degFileName;
  int M = -1, N = -1;
  bool verbose = true;
  unsigned long int seed = 0;

  const int OUTPUT_MODE_H_COMPRESSED = 0;
  const int OUTPUT_MODE_H = 1;
  const int OUTPUT_MODE_G_H_COMPRESSED = 2;
  int output_mode = OUTPUT_MODE_H_COMPRESSED; // default

  if (argc<9) {
    usage();
  }else {
    for(int i=1;i<argc;++i){
      if (strcmp(argv[i], "-numM")==0) {
	if (++i >= argc) usage();
	M=atoi(argv[i]);
      } else if(strcmp(argv[i], "-numN")==0) {
	if (++i >= argc) usage();
	N=atoi(argv[i]);
      } else if(strcmp(argv[i], "-codeName")==0) {
	if (++i >= argc) usage();
	codeName = argv[i];
      } else if(strcmp(argv[i], "-degFileName")==0) {
	if (++i >= argc) usage();
	degFileName = argv[i];
      } else if(strcmp(argv[i], "-sglConcent")==0) {
	if (++i >= argc) usage();
	sglConcent=atoi(argv[i]);
      } else if(strcmp(argv[i], "-tgtGirth")==0) {
	if (++i >= argc) usage();
	targetGirth=atoi(argv[i]);
      } else if(strcmp(argv[i], "-outputMode")==0) {
	if (++i >= argc) usage();
	output_mode=atoi(argv[i]);
      } else if(strcmp(argv[i], "-q")==0) {
	verbose=false;
			} else if(strcmp(argv[i], "-seed")==0) {
	if (++i >= argc) usage();
	seed=strtoul(argv[i],NULL,0);
      } else{
	usage();
      }
    }
    if (M == -1 || N == -1) {
      cout<<"Error: M or N not specified!"<<endl;
      exit(-1);
    }
    if (M>N) {
      cout<<"Error: M must be smaller than N!"<<endl;
      exit(-1);
    }
  }

  std::vector<int> degSeq(N);

  ifstream infn(degFileName.c_str());
  if (!infn) {cout << "\nCannot open file " << degFileName << endl; exit(-1); }
  int m;
  infn >>m;
  std::vector<int> deg(m);
  std::vector<double> degFrac(m);
  for(int i=0;i<m;i++) infn>>deg[i];
  for(int i=0;i<m;i++) infn>>degFrac[i];
  infn.close();
  double dtmp=0.0;
  for(int i=0;i<m;i++) dtmp+=degFrac[i];
  cout.setf(ios::fixed, ios::floatfield);
  if(abs(dtmp-1.0)>EPS) {
    cout.setf(ios::fixed, ios::floatfield);
    cout <<"\n Invalid degree distribution (node perspective): sum != 1.0 but "<<setprecision(10)<<dtmp<<endl; exit(-1);
  }
  for(int i=1;i<m;++i) degFrac[i]+=degFrac[i-1];
  for(int i=0;i<N;++i) {
    dtmp=double(i)/double(N);
    int j;
    for(j=m-1;j>=0;--j) {
      if(dtmp>degFrac[j]) break;
    }
    if(dtmp<degFrac[0]) degSeq[i]=deg[0];
    else degSeq[i]=deg[j+1];
  }

  BigGirth bigGirth(M, N, &degSeq[0], codeName.c_str(),
		    sglConcent, targetGirth, seed, verbose);

  switch(output_mode)
  {
	case OUTPUT_MODE_H_COMPRESSED: bigGirth.writeToFile_Hcompressed(); break;
  	case OUTPUT_MODE_H:   //  different output format
		bigGirth.writeToFile_Hmatrix(); break;
	case OUTPUT_MODE_G_H_COMPRESSED:
	//  different output format: including generator matrix (compressed)
		bigGirth.writeToFile(); break;
	default:
		cout << "Error: invalid output mode specified." << endl << endl;
		usage();
  }

  //computing local girth distribution

  if (verbose && N<10000) {
    cout<<" Now computing the local girth on the global Tanner graph setting. "<<endl;
    cout<<"     might take a bit long time. Please wait ...                   "<<endl;
    bigGirth.loadH();
    CyclesOfGraph cog(M, N, bigGirth.H);
    cog.getCyclesTable();
    cog.printCyclesTable();
  }
}

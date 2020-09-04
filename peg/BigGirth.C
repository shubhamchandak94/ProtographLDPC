#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include "BigGirth.h"

using namespace std;

NodesInGraph::NodesInGraph(void) {
  connectionParityBit=NULL;
  connectionSymbolBit=NULL;
}

void NodesInGraph::setNumOfConnectionSymbolBit(int deg) {
  if(deg<=0) {cout<<"Wrong NodesInGraph::setNumOfConnectionSymbolBit()"<<endl;exit(-1);}
  numOfConnectionSymbolBit=deg;
  connectionSymbolBit=new int[deg];
}
void NodesInGraph::initConnectionParityBit(void) {
  maxDegParity=10000;
  numOfConnectionParityBit=0;
  connectionParityBit=new int[1];//dummy memory, actually not used
}
void NodesInGraph::initConnectionParityBit(int deg) {
  maxDegParity=deg;
  numOfConnectionParityBit=0;
  connectionParityBit=new int[1];//dummy memory, actually not used
}
NodesInGraph::~NodesInGraph(void) {
    delete [] connectionParityBit;
    delete [] connectionSymbolBit;
}

BigGirth::BigGirth(void) : H(NULL), verbose(true) { }

BigGirth::BigGirth(int M, int N, int *symbolDegSequence,
									const char *filename, int sglConcent, int tgtGirth, unsigned long int seed,
									bool verbose_) : H(NULL), random_generator(seed), verbose(verbose_) {
  int i, j, k, m, index, localDepth=100;
  int *mid;

  EXPAND_DEPTH=(tgtGirth-4)/2;
  if(EXPAND_DEPTH<0) EXPAND_DEPTH=0;

  //      corresponds to depth l in the PEG paper;
  //      the target girth = 2*EXPAND_DEPTH+4
  //      if set large, then GREEDY algorithm

  this->M=M;
  this->N=N;
  this->filename=filename;

  mid=new int[M];

  localGirth=new int[N];

  nodesInGraph=new NodesInGraph [N];
  for(i=0;i<N;i++)
    nodesInGraph[i].setNumOfConnectionSymbolBit(symbolDegSequence[i]);

  j=0;
  for(k=0;k<N;k++) j+=symbolDegSequence[k];
  k=j/M;
  for(i=0;i<M;i++) mid[i]=k;
  for(i=0;i<j-k*M;i++) mid[i]++;
  k=0; for(i=0;i<M;i++) k+=mid[i];
  if(k!=j) {cout<<"Wrong in computing maxDegParity!"<<endl;exit(-1);}

  for(i=0;i<M;i++) {
    if(sglConcent==0) nodesInGraph[i].initConnectionParityBit(mid[i]);
    else  nodesInGraph[i].initConnectionParityBit();
  }

  for(k=0;k<N;k++){
    m=1000000;index=-1;
    for(i=0;i<M;i++){
      if(nodesInGraph[i].numOfConnectionParityBit<m && nodesInGraph[i].numOfConnectionParityBit<nodesInGraph[i].maxDegParity) {
	m=nodesInGraph[i].numOfConnectionParityBit;
	index=i;
      }
    }
    nodesInGraph[k].connectionSymbolBit[0]=index;//least connections of parity bit

    int iter=0;
  ITER:
    localGirth[k]=100;
    for(m=1;m<nodesInGraph[k].numOfConnectionSymbolBit;m++){
      nodesInGraph[k].connectionSymbolBit[m]=selectParityConnect(k, m, localDepth);
      localGirth[k]=(localGirth[k]>localDepth)?localDepth:localGirth[k];
      if(k>0 && localGirth[k]<localGirth[k-1] && iter<20) {iter++; goto ITER;}
      if(localGirth[k]==0 && iter<30) {iter++; goto ITER;}
    }
    //if((k+1)%100==0) {
    if(verbose) {
      cout<<"k="<<k<<"  ";
      for(m=0;m<nodesInGraph[k].numOfConnectionSymbolBit;m++)
	cout<<nodesInGraph[k].connectionSymbolBit[m]<<" ";
      cout<<"LocalGirth="<<2*localGirth[k]+4;
      cout<<endl;
    }
    updateConnection(k);
  }

  if(verbose) {
    cout<<"Showing the row weight distribution..."<<endl;
    for(i=0;i<M;i++)
      cout<<nodesInGraph[i].numOfConnectionParityBit<<" ";
    cout<<endl;
  }
  delete [] mid;

	if(verbose) {
	  ofstream cycleFile;
	  cycleFile.open("leftHandGirth.log", ios::out);
	  localDepth=100;
	  for(k=0;k<N;k++) {
	    if(localGirth[k]<localDepth) localDepth=localGirth[k];
	    if(localDepth==100) cycleFile<<"inf ";
	    else cycleFile<<2*localDepth+4<<" ";
	  }
	  cycleFile<<endl;
	  cycleFile.close();

    cout<<"*************************************************************"<<endl;
    cout<<"       The global girth of the PEG Tanner graph :="<< 2*localDepth+4<<endl;
    cout<<"*************************************************************"<<endl;
  }

  loadH();

}

BigGirth::~BigGirth(void) {
  if(H!=NULL) {
    for(int i=0;i<M;i++)
      delete [] H[i];
    delete [] H;
    H=NULL;
  }
  delete [] localGirth;
  delete [] nodesInGraph;
  nodesInGraph=NULL;
}

int BigGirth::selectParityConnect(int kthSymbol, int mthConnection, int & cycle) {
  int i, j, k, index, mincycles, numCur, cpNumCur;
  int *tmp, *med;
  int *current;//take note of the covering parity bits

  mincycles=0;
  tmp=new int[M]; med=new int[M];

  numCur=mthConnection;
  current=new int[mthConnection];
  for(i=0;i<mthConnection;i++) current[i]=nodesInGraph[kthSymbol].connectionSymbolBit[i];

LOOP:
  mincycles++;
  for(i=0;i<M;i++) tmp[i]=0;
  //maintain
  for(i=0;i<mthConnection;i++) tmp[nodesInGraph[kthSymbol].connectionSymbolBit[i]]=1;
  for(i=0;i<numCur;i++){
    for(j=0;j<nodesInGraph[current[i]].numOfConnectionParityBit;j++){
      for(k=0;k<nodesInGraph[nodesInGraph[current[i]].connectionParityBit[j]].numOfConnectionSymbolBit;k++){
        tmp[nodesInGraph[nodesInGraph[current[i]].connectionParityBit[j]].connectionSymbolBit[k]]=1;
      }
    }
  }

  index=0; cpNumCur=0;
  for(i=0;i<M;i++) {
    if(tmp[i]==1) cpNumCur++;
    if(tmp[i]==1 || nodesInGraph[i].numOfConnectionParityBit>=nodesInGraph[i].maxDegParity)
      index++;
  }
  if(cpNumCur==numCur) {//can not expand any more
    //additional handlement to select one having least connections
    j=10000000; //dummy number
    for(i=0;i<M;i++){
      if(tmp[i]==0 && nodesInGraph[i].numOfConnectionParityBit<j && nodesInGraph[i].numOfConnectionParityBit<nodesInGraph[i].maxDegParity)
	j=nodesInGraph[i].numOfConnectionParityBit;
    }
    for(i=0;i<M;i++){
      if(tmp[i]==0){
	if(nodesInGraph[i].numOfConnectionParityBit!=j || nodesInGraph[i].numOfConnectionParityBit>=nodesInGraph[i].maxDegParity){
	  tmp[i]=1;
	}
      }
    }
    index=0;
    for(i=0;i<M;i++) if(tmp[i]==1) index++;
    //----------------------------------------------------------------
		std::uniform_int_distribution<int> distribution(0,M-index-1);
    j=distribution(random_generator)+1;
    index=0;
    for(i=0;i<M;i++){
      if(tmp[i]==0) index++;
      if(index==j) break;
    }
    delete [] tmp; tmp=NULL;
    delete [] current; current=NULL;
    return(i);
  }
  else if(index==M || mincycles>EXPAND_DEPTH){//covering all parity nodes or meet the upper bound on cycles

    cycle=mincycles-1;
    for(i=0;i<M;i++) tmp[i]=0;
    for(i=0;i<numCur;i++) tmp[current[i]]=1;
    index=0;
    for(i=0;i<M;i++) if(tmp[i]==1) index++;
    if(index!=numCur) {cout<<"Error in the case of (index==M)"<<endl;exit(-1);}
    //additional handlement to select one having least connections
    j=10000000;
    for(i=0;i<M;i++){
      if(tmp[i]==0 && nodesInGraph[i].numOfConnectionParityBit<j && nodesInGraph[i].numOfConnectionParityBit<nodesInGraph[i].maxDegParity)
	j=nodesInGraph[i].numOfConnectionParityBit;
    }
    for(i=0;i<M;i++){
      if(tmp[i]==0){
	if(nodesInGraph[i].numOfConnectionParityBit!=j || nodesInGraph[i].numOfConnectionParityBit>=nodesInGraph[i].maxDegParity){
	  tmp[i]=1;
	}
      }
    }

    index=0;
    for(i=0;i<M;i++) if(tmp[i]==1) index++;

		std::uniform_int_distribution<int> distribution(0,M-index-1);
    j=distribution(random_generator)+1;
    index=0;
    for(i=0;i<M;i++){
      if(tmp[i]==0) index++;
      if(index==j) break;
    }
    delete [] tmp; tmp=NULL;
    delete [] current; current=NULL;
    return(i);
  }
  else if(cpNumCur>numCur && index!=M){
    delete [] current;
    current=NULL;
    numCur=cpNumCur;
    current=new int[numCur];
    index=0;
    for(i=0;i<M;i++) {
      if(tmp[i]==1) {current[index]=i; index++;}
    }
    goto LOOP;
  }
  else {
    cout<<"Should not come to this point..."<<endl;
    cout<<"Error in BigGirth::selectParityConnect()"<<endl;
    return(-1);
  }
}


void BigGirth::updateConnection(int kthSymbol){
  int i, j, m;
  int *tmp;

  for(i=0;i<nodesInGraph[kthSymbol].numOfConnectionSymbolBit;i++){
    m=nodesInGraph[kthSymbol].connectionSymbolBit[i];//m [0, M) parity node
    tmp=new int[nodesInGraph[m].numOfConnectionParityBit+1];
    for(j=0;j<nodesInGraph[m].numOfConnectionParityBit;j++)
      tmp[j]=nodesInGraph[m].connectionParityBit[j];
    tmp[nodesInGraph[m].numOfConnectionParityBit]=kthSymbol;

    delete [] nodesInGraph[m].connectionParityBit;
    nodesInGraph[m].connectionParityBit=NULL;
    nodesInGraph[m].numOfConnectionParityBit++; //increase by 1
    nodesInGraph[m].connectionParityBit=new int[nodesInGraph[m].numOfConnectionParityBit];
    for(j=0;j<nodesInGraph[m].numOfConnectionParityBit;j++)
      nodesInGraph[m].connectionParityBit[j]=tmp[j];
    delete [] tmp;
    tmp=NULL;
  }
}

void BigGirth::loadH(void){
  int i, j;
  if(H==NULL) {
    H=new int*[M];
    for(i=0;i<M;i++) H[i]=new int[N];
  }

  for(i=0;i<M;i++){
    for(j=0;j<N;j++){
      H[i][j]=0;
    }
  }
  for(i=0;i<M;i++){
    for(j=0;j<nodesInGraph[i].numOfConnectionParityBit;j++){
      H[i][nodesInGraph[i].connectionParityBit[j]]=1;
    }
  }
}

void BigGirth::writeToFile_Hmatrix(void){
  int i, j;

  loadH();

  //cout<<"---------------code format--------------------------"<<endl;
  //cout<<"-            Block length N                        -"<<endl;
  //cout<<"-            Num of Check Nodex M                  -"<<endl;
  //cout<<"-            H matrix                              -"<<endl;
  //cout<<"----------------------------------------------------"<<endl;

  ofstream codefile;
  codefile.open(filename,ios::out);
  codefile<<N<<" "<<M<<endl;

  for(i=0;i<M;i++){
    for(j=0;j<N;j++){
      codefile<<H[i][j]<<" ";
    }
    codefile<<endl;
  }
  codefile.close();
}

void BigGirth::writeToFile_Hcompressed(void){
  int i, j, max_col;
  int *(*parityCheck_compressed);

  //cout<<"---------------code format--------------------------"<<endl;
  //cout<<"-            Block length N                        -"<<endl;
  //cout<<"-            Num of Check Nodex M                  -"<<endl;
  //cout<<"-            Num of column in the compressed H     -"<<endl;
  //cout<<"-            H matrix (compressed)                 -"<<endl;
  //cout<<"----------------------------------------------------"<<endl;

  //finding the num of columns, l, of the compressed parity-check matrix

  max_col=0;
  for(i=0;i<M;i++)
    if(nodesInGraph[i].numOfConnectionParityBit>max_col)
      max_col=nodesInGraph[i].numOfConnectionParityBit;

  parityCheck_compressed=new int * [M];
  for(i=0;i<M;i++)
    parityCheck_compressed[i]=new int[max_col];
  for(i=0;i<M;i++){
    for(j=0;j<max_col;j++) parityCheck_compressed[i][j]=0;
    for(j=0;j<nodesInGraph[i].numOfConnectionParityBit;j++){
      parityCheck_compressed[i][j]=nodesInGraph[i].connectionParityBit[j]+1;
    }
  }

  ofstream codefile;
  codefile.open(filename,ios::out);
  codefile<<N<<endl;
  codefile<<M<<endl;
  codefile<<max_col<<endl;
  for(i=0;i<M;i++){
    for(j=0;j<max_col;j++)
      codefile<<parityCheck_compressed[i][j]<<" ";
    codefile<<endl;
  }
  codefile.close();

  for(i=0;i<M;i++){
    delete [] parityCheck_compressed[i];
    parityCheck_compressed[i]=NULL;
  }
  delete [] parityCheck_compressed;
  parityCheck_compressed=NULL;
}

void BigGirth::writeToFile(void){
  int i, j, k, d, redun;
  int imed, max_row, index, max_col;
  int *Index, *J, *itmp, *(*generator), *(*generator_compressed), *(*parityCheck_compressed);
  //Gaussian Ellimination
  Index=new int[M];
  J=new int[N];
  itmp=new int[N];
  for(i=0;i<M;i++) Index[i]=0; //indicator of redudant rows
  for(j=0;j<N;j++) J[j]=j; //column permutation
  redun=0;//the number of redundant rows

  loadH();

  for(k=0;k<M;k++){
    if(H[k][J[k-redun]]==0) {
      d=k;
      for(i=k+1-redun;i<N;i++)
	if(H[k][J[i]]!=0) {d=i;break;}
      if(d==k) {//full-zero row:delete this row
	redun++;
	Index[k]=1;
	continue;
      }
      else {//SWAP d column and k column in H matrix
	imed=J[k-redun];
	J[k-redun]=J[d];
	J[d]=imed;
      }
    }
    if(H[k][J[k-redun]]==0) {
      cout<<"ERROR: should not come to this point"<<endl;
      exit(-1);
    }
    else {
      for(i=k+1;i<M;i++){
	if(H[i][J[k-redun]]!=0){
	  for(j=k-redun;j<N;j++)
	    H[i][J[j]]=(H[i][J[j]]+H[k][J[j]])%2;
	}
      }
    }
  }

  if(verbose)
    cout<<"Row rank of parity check matrix="<<M-redun<<endl;

  K=N-M+redun;//num of the information bits

  index=0;
  for(i=0;i<M;i++){
    if(Index[i]==0){ // all-zero row
      for(j=0;j<N;j++)
	itmp[j]=H[i][J[j]];
      for(j=0;j<N;j++)
	H[index][j]=itmp[j]; //Note: itmp can not be omitted here!!!
      index++;
    }
  }
  if(index!=M-redun) {cout<<"ERROR...if(index!=M-redun)"<<endl;exit(-1);}

  for(k=index-1;k>0;k--){
    for(i=k-1;i>=0;i--){
      if(H[i][k]==1)
	for(j=k;j<N;j++)
	  H[i][j]=(H[i][j]+H[k][j])%2;
    }
  }

  if(verbose) {
    cout<<"****************************************************"<<endl;
    cout<<"      Computing the compressed generator"<<endl;
    cout<<"****************************************************"<<endl;
  }
  generator=new int * [K];
  for(i=0;i<K;i++)
    generator[i]=new int[N-K];
  for(i=0;i<K;i++){
    for(j=0;j<N-K;j++)
      generator[i][j]=H[j][i+N-K];
    //for(j=N-K;j<N;j++)
    //generator[i][j]=0;
    //generator[i][i+N-K]=1;
  }
  max_row=0;
  for(j=0;j<N-K;j++){
    imed=0;
    for(i=0;i<K;i++)
      imed+=generator[i][j];
    if(imed>max_row) max_row=imed;
  }
  generator_compressed=new int * [max_row];
  for(i=0;i<max_row;i++)
    generator_compressed[i]=new int[N];
  for(j=0;j<N-K;j++){
    index=0;
    for(i=0;i<max_row;i++)  generator_compressed[i][j]=0;
    for(i=0;i<K;i++){
      if(generator[i][j]==1) {
	generator_compressed[index][j]=i+1;
	if(index>=max_row-1) break;
	index++;
      }
    }
  }
  for(j=0;j<K;j++){
    for(i=0;i<max_row;i++) generator_compressed[i][j+N-K]=0;
    generator_compressed[0][j+N-K]=j+1;
  }
  if(verbose) {
    cout<<"*****************************************************"<<endl;
    cout<<"     Computing the compressed parity-check matrix"<<endl;
    cout<<"*****************************************************"<<endl;
  }
  //finding the num of columns, l, of the compressed parity-check matrix
  loadH(); //loading parity check matrix again
  max_col=0;
  for(i=0;i<M;i++){
    imed=0;
    for(j=0;j<N;j++)
      imed+=H[i][j];
    if(imed>max_col) max_col=imed;
  }
  parityCheck_compressed=new int * [M];
  for(i=0;i<M;i++)
    parityCheck_compressed[i]=new int[max_col];
  for(i=0;i<M;i++){
    for(j=0;j<max_col;j++) parityCheck_compressed[i][j]=0;
    index=0;
    for(j=0;j<N;j++){
      if(H[i][J[j]]==1) {
	parityCheck_compressed[i][index]=j+1;
	if(index>=max_col-1) break;
	index++;
      }
    }
  }
  if(verbose) {
    cout<<"****************************************************"<<endl;
    cout<<"      Write to file (TEXT!) "<<endl;
    cout<<"****************************************************"<<endl;
  }
  ofstream codefile;
  codefile.open(filename,ios::out);
  codefile<<N<<endl;
  codefile<<K<<endl;
  codefile<<M<<endl;
  codefile<<max_row<<endl;
  codefile<<max_col<<endl;
  for(i=0;i<max_row;i++){
    for(j=0;j<N;j++)
      codefile<<generator_compressed[i][j]<<" ";
    codefile<<endl;
  }
  for(i=0;i<M;i++){
    for(j=0;j<max_col;j++)
      codefile<<parityCheck_compressed[i][j]<<" ";
    codefile<<endl;
  }
  for(i=N-K;i<N;i++)
    codefile<<i+1<<" ";
  codefile<<endl;

  codefile.close();
  if(verbose) {
    cout<<"****************************************************"<<endl;
    cout<<"      Free memory"<<endl;
    cout<<"****************************************************"<<endl;
  }
  delete [] Index;
  Index=NULL;
  delete [] J;
  J=NULL;
  delete [] itmp;
  itmp=NULL;
  for(i=0;i<M;i++){
    delete [] parityCheck_compressed[i];
    parityCheck_compressed[i]=NULL;
  }
  delete [] parityCheck_compressed;
  parityCheck_compressed=NULL;
  for(i=0;i<max_row;i++){
    delete [] generator_compressed[i];
    generator_compressed[i]=NULL;
  }
  delete [] generator_compressed;
  generator_compressed=NULL;
  for(i=0;i<K;i++){
    delete [] generator[i];
    generator[i]=NULL;
  }
  delete [] generator;
  generator=NULL;

  if(verbose) {
    cout<<"****************************************************"<<endl;
    cout<<"      OK!"<<endl;
    cout<<"****************************************************"<<endl;
  }

}

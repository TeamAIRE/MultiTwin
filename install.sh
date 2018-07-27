#!/usr/bin/env bash

# multitwin directory
MULTITWINDIR=$(pwd)

# Change owner
chown -R $USER:$USER $MULTITWINDIR

# checking Python version
if [[ $(which python3) != "/usr/bin/python3" ]]; then
    echo "No python3 found: please contact your system administrator";
    exit;
fi

# Checking g++ compiler
G=$(g++ --version | head -n1) 
GVERSION=$(echo $G | cut -d" " -f3 | cut -d"-" -f1 | gawk '{split($0,a,"."); print a[1]"."a[2]>=4.8}')
if [[ $GVERSION == 0 ]]; then
    echo "Update version of g++ compiler to >= 4.8
    Check for instructions in the INSTALL file."; exit;
else echo "Version of $G: ok ";
fi

if [[ -n $(ls /usr/local/lib | grep libigraph.so.0) && -n $(ls /usr/local/include | grep igraph) ]]; then
    echo "igraph correctly installed"
else
    echo "Check igraph installation: see INSTALL file"; exit
fi;

python3 -m pip install python-igraph
python3 -m pip install ttkthemes
python3 -m pip install bs4
python3 -m pip install --upgrade html5lib

# install blast and diamond
if [[ -n $MULTITWINDIR/simtools ]]; then rm -rf $MULTITWINDIR/simtools; fi 
mkdir -p $MULTITWINDIR/simtools
cd $MULTITWINDIR/simtools/
# install blast
BLASTVERSION="2.7.1"
echo "#Installing BLAST $BLASTVERSION"
wget -q ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/$BLASTVERSION/ncbi-blast-$BLASTVERSION+-x64-linux.tar.gz
tar -xzf "ncbi-blast-$BLASTVERSION"+-x64-linux.tar.gz
rm "ncbi-blast-$BLASTVERSION"+-x64-linux.tar.gz
mv $MULTITWINDIR/simtools/ncbi-blast-$BLASTVERSION+ $MULTITWINDIR/simtools/blast

DIAMONDVERSION="v0.9.22"
echo "#Installing DIAMOND $DIAMONDVERSION"
mkdir -p $MULTITWINDIR/simtools/diamond
cd $MULTITWINDIR/simtools/diamond
wget -q https://github.com/bbuchfink/diamond/releases/download/$DIAMONDVERSION/diamond-linux64.tar.gz
tar -xzf diamond-linux64.tar.gz
rm diamond-linux64.tar.gz

cd $MULTITWINDIR

# install exonerate
if [[ -n $MULTITWINDIR/exonerate ]]; then rm -rf $MULTITWINDIR/exonerate; fi 
echo "#Installing EXONERATE 2.2.0"
wget -q http://ftp.ebi.ac.uk/pub/software/vertebrategenomics/exonerate/exonerate-2.2.0-x86_64.tar.gz
tar -xzf exonerate-2.2.0-x86_64.tar.gz
mv $MULTITWINDIR/exonerate-2.2.0-x86_64 $MULTITWINDIR/exonerate
rm $MULTITWINDIR/exonerate-2.2.0-x86_64.tar.gz

BASHRC=$HOME/.bashrc

# add to bashrc
echo "# These lines have been written by the MULTITWIN install.sh file" >> $BASHRC
echo "export LD_LIBRARY_PATH=$LD_LIBARY_PATH:/usr/local/lib" >> $BASHRC
echo "export MT_BLAST=$MULTITWINDIR/simtools/blast/bin" >> $BASHRC
echo "export MT_DIAMOND=$MULTITWINDIR/simtools/diamond" >> $BASHRC
echo "export MT_EXONERATE=$MULTITWINDIR/exonerate/bin" >> $BASHRC
echo "export PATH=$MULTITWINDIR/python-scripts:\$PATH" >> $BASHRC
echo "export PATH=$MULTITWINDIR/BlastProg:\$PATH" >> $BASHRC
echo "# END of MULTITWIN install section"  >> $BASHRC
cd BlastProg/
make

cd $MULTITWIN
# END


while IFS=" " read -r mol;
do
# convert gaussian log files to mol2
antechamber -i "$mol".log -fi gout -o "$mol".gcrt -fo gcrt -pf yes
#antechamber -i "$mol".pdb -fi pdb -o "$mol".mol2 -fo mol2 -pf yes
# convert mol2 format to pdbm format
#antechamber -i "$mol".mol2 -fi mol2 -o "$mol".gcrt -fo gcrt -pf yes
done < files

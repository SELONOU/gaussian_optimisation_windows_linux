#Generate ESP after optimization
while read -r ligand;
do
obabel "$ligand".pdb -O "$ligand".xyz

sed -i '1,2d' "$ligand".xyz
echo "" >empty
echo "%mem=90GB" >link0
echo "%nprocshared=48" >>link0
echo "%chk=""$ligand""_ESP.chk" >> last_frame_100ps_200_water_"$ligand"_split_1_ESP.com
echo "#p HF/6-31G* Pop=(MK) IOp(6/50=1)"> route_scfesp
echo "title goes here">title
echo "0 1" >charge
        cp $ligand".xyz"  coordinate
	echo "last_frame_100ps_200_water_"$ligand"_split_1.esp" >additionalline

        cat link0 route_scfesp empty title empty charge coordinate empty additionalline empty >> last_frame_100ps_200_water_"$ligand"_split_1_ESP.com
        rm empty link0 route_scfesp title charge coordinate additionalline


done < file.txt


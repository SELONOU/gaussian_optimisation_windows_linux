for i in {1..21..1};
do
#sed -i '1d' Mol"$i".gjf
#cat criteria Mol"$i".gjf > mol"$i".com
#sed -i 's/name.chk/mol'"$i"'.chk/g' mol"$i".com
g16 <mol"$i".com> mol"$i".log
done

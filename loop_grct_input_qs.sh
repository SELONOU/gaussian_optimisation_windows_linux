while IFS=" " read -r mol;
do
sed -i '1,3d' "$mol".gcrt
cat criteria_truba_qs "$mol".gcrt > "$mol".gjf
sed -i 's/%chk=molsp.chk/%chk='"$mol"'sp.chk/g' "$mol".gjf
sed -i 's/remark line goes here/'"$mol"'/g' "$mol".gjf
done < files

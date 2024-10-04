while IFS=" " read -r mol;
do
sed -i '1,3d' "$mol".gjf
cat criteria_truba "$mol".gjf > "$mol".com
sed -i '3s/.*/%chk='"$mol"'.chk/' "$mol".com # replace the entire 3rd line by %chk=
sed -i 's/Title Card Required/'"$mol"'/g' "$mol".com
done < files

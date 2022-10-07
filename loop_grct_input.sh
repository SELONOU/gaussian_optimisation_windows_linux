while IFS=" " read -r mol;
do
sed -i '1,3d' "$mol".gcrt
cat criteria_truba "$mol".gcrt > "$mol".com
sed -i '3s/.*/%chk='"$mol"'sp.chk/' "$mol".com # replace the entire 3rd line by %chk=
sed -i 's/remark line goes here/'"$mol"'/g' "$mol".com
done < files

echo "%mem=10GB" >tmp
echo "%nprocshared=112" >>tmp
echo "%nosave" >>tmp
echo "# opt b3lyp/6-31g(d,p) geom=connectivity gfoldprint int=nofofcou iop(3/33=1)" >>tmp
echo "" >>tmp
echo "title goes here" >>tmp
echo "">>tmp
echo "0 1">>tmp


for file in *.xyz
do
        fn="${file%.*}"
        echo "%chk=""$fn"".chk" >tmp1
        tail -n +3 <"$fn".xyz >tmp2
        echo "" >>tmp2
        echo "" >>tmp2
        cat tmp1 tmp tmp2 > "$fn".com
        rm tmp1 tmp2
done

rm *.xyz tmp

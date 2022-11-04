set encoding utf8
set terminal png size 820, 640
set output "img/hash_inc_amount_10_and_4.png"

set grid xtics lc rgb '#555555' lw 1 lt 0
set grid ytics lc rgb '#555555' lw 1 lt 0
set xlabel 'Название файла'
set ylabel 'Количество хешей'

set style line 1 \
linecolor rgb '#ff9000' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 2 \
linecolor rgb '#ffcc89' \
linetype 1 linewidth 2 \
pointtype 7 pointsize 1

set xtics rotate by 30 right
set ylabel offset -2,0

set lmargin at screen 0.16
set bmargin at screen 0.23
set rmargin at screen 0.97
set tmargin at screen 0.97

set offset 0.2,0.2,0,0

set key left top

plot 'results/hash_inc_amount_4_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 1 ti 'none (4 byte)', \
     'results/hash_inc_amount_10_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 2 ti 'none (10 byte)', \

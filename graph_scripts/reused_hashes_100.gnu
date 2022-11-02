set encoding utf8
set terminal png size 640, 800
set output "img/reused_hashes_100.png"

set grid xtics lc rgb '#555555' lw 1 lt 0
set grid ytics lc rgb '#555555' lw 1 lt 0
set xlabel 'Название файла'
set ylabel 'Количество хешей'

set style line 1 \
linecolor rgb '#ff9000' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 2 \
linecolor rgb '#005aff' \
linetype 1 linewidth 2 \
pointtype 7 pointsize 1

set style line 3 \
linecolor rgb '#ff006f' \
linetype 1 linewidth 2 \
pointtype 9 pointsize 1

set xtics rotate by 70 right

set key left top

plot 'results/reused_hashes_100_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 1 ti 'none', \
     'results/reused_hashes_100_3_MD5.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 2 ti 'MD5', \
     'results/reused_hashes_100_3_sha1.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 3 ti 'SHA1', \
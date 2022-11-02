set encoding utf8
set terminal png size 640, 800
set output "img/hash_inc_amount_all.png"

set grid xtics lc rgb '#555555' lw 1 lt 0
set grid ytics lc rgb '#555555' lw 1 lt 0
set xlabel 'Название файла'
set ylabel 'Количество хешей'

set yrange [0:3500000]

set style line 1 \
linecolor rgb '#ff8f00' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 2 \
linecolor rgb '#ff0070' \
linetype 1 linewidth 2 \
pointtype 7 pointsize 1

set style line 3 \
linecolor rgb '#00ff8f' \
linetype 1 linewidth 2 \
pointtype 9 pointsize 1

set style line 4 \
linecolor rgb '#00f0ff' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 5 \
linecolor rgb '#f0ff00' \
linetype 1 linewidth 2 \
pointtype 7 pointsize 1

set style line 6 \
linecolor rgb '#8f00ff' \
linetype 1 linewidth 2 \
pointtype 9 pointsize 1

set style line 7 \
linecolor rgb '#ff00f0' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 8 \
linecolor rgb '#ffb14d' \
linetype 1 linewidth 2 \
pointtype 7 pointsize 1

set style line 9 \
linecolor rgb '#ff4d9b' \
linetype 1 linewidth 2 \
pointtype 9 pointsize 1

set style line 10 \
linecolor rgb '#00a8b3' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1

set style line 11 \
linecolor rgb '#a8b300' \
linetype 1 linewidth 2 \
pointtype 5 pointsize 1


set xtics rotate by 70 right

set key left top

plot 'results/hash_inc_amount_100_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 1 ti 'none (100 byte)', \
     'results/hash_inc_amount_100_3_MD5.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 2 ti 'MD5 (100 byte)', \
     'results/hash_inc_amount_100_3_sha1.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 3 ti 'SHA1 (100 byte)', \
     'results/hash_inc_amount_50_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 4 ti 'none (50 byte)', \
     'results/hash_inc_amount_50_3_MD5.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 5 ti 'MD5 (50 byte)', \
     'results/hash_inc_amount_50_3_sha1.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 6 ti 'SHA1 (50 byte)', \
     'results/hash_inc_amount_20_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 7 ti 'none (20 byte)', \
     'results/hash_inc_amount_20_3_MD5.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 8 ti 'MD5 (20 byte)', \
     'results/hash_inc_amount_20_3_sha1.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 9 ti 'SHA1 (20 byte)', \
     'results/hash_inc_amount_4_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 10 ti 'none (4 byte)', \
     'results/hash_inc_amount_10_3_None.txt' using 2:xticlabels(1) index 0 with linespoints linestyle 11 ti 'none (10 byte)', \

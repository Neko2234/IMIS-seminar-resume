#!/usr/bin/env perl

# $latex = 'uplatex';
# $bibtex = 'upbibtex';
# $dvipdf = 'dvipdfmx %O -o %D %S';
# $makeindex = 'mendex -U %O -o %D %S';
# $pdf_mode = 3; 
# $ENV{'TZ'} = 'Asia/Tokyo';
# $ENV{OPENTYPEFONTS} = '/usr/share/fonts//:';
# $ENV{TTFONTS} = '/usr/share/fonts//:';

$do_cd = 1;

$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
# $latex = 'platex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$latex = 'uplatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S';
$lualatex = 'lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error --shell-escape %S';
$dvipdf = 'dvipdfmx %O -o %D %S';
$makeindex = 'makeindex %O -o %D %S';

$bibtex_use=2;
$bibtex = 'upbibtex %O %S';
$biber = 'biber --bblencoding=utf8 -u -U --output_safechars %O %S';

$clean_ext="$clean_ext run.xml";

# pdflatexは1,uplatexは3,lualatexは4
$pdf_mode = 3;
$max_repeat = 10;

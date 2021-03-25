from bs4 import BeautifulSoup
import get_france_coronavirus

html_toread='france_coronavirus.html'  # file created by get_france_coronavirus.py
html_towrite='france_death.html'

header = '''<link href="bootstrap.min.css" rel="stylesheet">
            <link href="wm16.css" rel="stylesheet">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/dataTables.bootstrap.min.css" />

            <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
            <script src="bootstrap.min.js"></script>
            <script src="https://code.highcharts.com/highcharts.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
            <script type="text/javascript" src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js"></script>
            <script type="text/javascript" class="init">
                $.extend( $.fn.dataTable.defaults, {
                    responsive: true
                } );
                    
                    $(document).ready(function() {
                    $('#example2').dataTable( {
                        "scrollCollapse": true,
                        "sDom": '<"bottom"flp><"clear">',
                        "paging":         false
                    } );
                } );
                    </script>
            <script type="text/javascript" class="init">
                $.extend( $.fn.dataTable.defaults, {
                    responsive: true
                } );
    
                $(document).ready(function() {
                $('#table3').dataTable( {
                    "scrollCollapse": true,
                             "order": [[ 1, 'desc' ]],
                    "sDom": '<"bottom"flp><"clear">',
                    "paging":         false
                } );
            } );
                </script>
            <script type="text/javascript" class="init">
                    $.extend( $.fn.dataTable.defaults, {
                responsive: true
            } );
                
                $(document).ready(function() {
                $('#example').dataTable( {
                    "scrollCollapse": true,
                    "searching": false,

                    "sDom": '<"top">rt<"bottom"flp><"clear">',
                    "paging":         false
                } );
            } );
                </script>
            <script type="text/javascript" class="init">
            $(document).ready(function() {
                $('#popbycountry').dataTable();
            } );
                </script>
'''    
    
js = '''<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <script src="bootstrap.min.js"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.10.19/js/dataTables.bootstrap.min.js"></script>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script>
            $(function() {

                $('.flip_cases_front').on('click', function() {


                    $(this).parent().parent().addClass('flip');
                });

                $('.flip_cases_back').on('click', function() {


                    $(this).parent().parent().removeClass('flip');
                });
            });
        </script>
        '''

links = '''<link href="bootstrap.min.css" rel="stylesheet">
            <link href="wm16.css" rel="stylesheet">\n'''
   
style ='''
        <style>
            .panel_flip {
                position: relative;
                height: 100%;
            }

            .panel_front {
                height: inherit;
                position: absolute;
                top: 0;
                -webkit-transform: rotateX(0deg) rotateY(0deg);
                -moz-transform: rotateX(0deg) rotateY(0deg);
                -webkit-transform-style: preserve-3d;
                -moz-transform-style: preserve-3d;
                -webkit-backface-visibility: hidden;
                -moz-backface-visibility: hidden;
                -webkit-transition: all .4s ease-in-out;
                -moz-transition: all .4s ease-in-out;
                -ms-transition: all .4s ease-in-out;
                -o-transition: all .4s ease-in-out;
                transition: all .4s ease-in-out;
            }
            .panel_back {
                height: inherit;
                position: absolute;
                top: 0;
                -webkit-transform: rotateY(-180deg);
                -moz-transform: rotateY(-180deg);
                -webkit-transform-style: preserve-3d;
                -moz-transform-style: preserve-3d;
                -webkit-backface-visibility: hidden;
                -moz-backface-visibility: hidden;
                -webkit-transition: all .4s ease-in-out;
                -moz-transition: all .4s ease-in-out;
                -ms-transition: all .4s ease-in-out;
                -o-transition: all .4s ease-in-out;
                transition: all .4s ease-in-out;
            }
            .panel_flip.flip .panel_front {
                z-index: 900;
                -webkit-transform: rotateY(180deg);
                -moz-transform: rotateY(180deg);
            }
            .panel_flip.flip .panel_back {
                z-index: 1000;
                -webkit-transform: rotateX(0deg) rotateY(0deg);
                -moz-transform: rotateX(0deg) rotateY(0deg);
            }
            .graph_row {

                margin-bottom: 20px;
            }
        </style>'''

def read_txt(file_name):
    f = open(file_name, "r")
    src = f.read()
    f.close()
    return src

def write_txt(file_name,text):
    f = open(file_name, "w")
    f.write(text)
    f.close()

src = read_txt(html_toread)
soup = BeautifulSoup(src, 'lxml')

#scripts = soup.find_all('script')
keys = ['Total Cases','Daily New Cases', 'Active Cases', 'Total Deaths', 'Daily Deaths','New Cases vs.','Outcome']
key = keys[4]
scripts = soup.find_all(class_='graph_row')
for s in scripts:
    if key in s.text :
        row = s
        break
#scripts = list(filter(lambda x: 'Highcharts' in x.text, scripts))

#text = header + style + str(daily_death)
text = js + links + style + str(row)
write_txt(html_towrite,text)

data=str(row).split('\n')
r = list(filter(lambda x: ('{' in x) or (':' in x) or ('}' in x), data))
r = [x.strip() for x in r]
r[0] = r[0].split("'")[1:]
dict_name=r[0][0]
r[0]=r[0][-1][-1]

json = ''   #'['+dict_name+'{'
for n in r:
    json += n.strip()

d={}
for x in r:
    if 'data:' in x or 'categories:' in x:
        x=x.split('}')
        x=x[0].split(':')
        d[x[0]]=x[1].strip()

z=d['categories'].split('"')
d['categories']=[x for x in z if len(x)>1]
w=d['data'][1:-1].split(',')
d['data']=[int(x) for x in w]

import matplotlib.pyplot as plt
import numpy as np

x=d['categories']
y=d['data']
plt.bar(x,y)
plt.xticks(np.arange(0, len(x), 5), rotation=45)
plt.show()

from scipy.interpolate import interp1d

x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')
xnew = np.linspace(0, 10, num=41, endpoint=True)
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()

y = d['data']   #d dictionary
x = np.linspace(0, len(y), len(y))
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')
xnew = np.linspace(0, len(y), 100*len(y))
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()

import pandas as pd
df = pd.DataFrame([d['categories'],d['data']]).T
df.rename(columns={0:'Date',1:'Daily Deaths'}, inplace=True)
df.set_index('Date',inplace=True)
df.plot.bar()
plt.xticks(rotation=45)
plt.show()

df['shift']=df['Daily Deaths'][20:].shift(1)
df['percent']=(df['Daily Deaths'][20:]/df['Daily Deaths'][20:].shift(1)-1)*100

df2=df[20:]
plt.bar(df2.index,df2['percent'])
plt.xticks(rotation=45)
plt.show()
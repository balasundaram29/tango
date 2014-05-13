#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      AnnaiAll
#
# Created:     02/04/2014
# Copyright:   (c) AnnaiAll 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')
from rango.models import Category,Page
def populate():
    python_cat=add_cat('Python',views=128,likes=64)
    add_page(python_cat,
	   title='Official Python Tutorial',
	   url='http://doc.python.org/2/tutorial',views=39)
    add_page(cat=python_cat,
       title='How to Think like a Computer Scientist',
       url='http://www.greenteapress.com/thinkpython/',views=39)

    add_page(cat=python_cat,
        title='Learn Python in 10 Minutes',
        url='http://www.korokithakis.net/tutorial/python/',views=39)

    django_cat=add_cat('Django',views=64,likes=32)
    add_page(cat=django_cat,
        title='Official Django Tutorial',
        url='https://docs.djangoprojects.com/en/15/intro/tutorial01/',views=97)

    add_page(cat=django_cat,
        title='Django Rocks',
        url='http://www.djangorocks.com/',views=79)

    add_page(cat=django_cat,
        title='How to Tango with Django',
        url='http://www.tangowithdjango.com/',views=24)

    frame_cat=add_cat('Other Frameworks',views=32,likes=16)

    add_page(cat=frame_cat,
        title='Bottle',
        url='http://bottlepy.com/docs/dev/',views=36)

    add_page(cat=frame_cat,
        title='Flask',
        url='http://flask/pocoo.org',views=31)

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1} ".format(str(c),str(p))

def add_page(cat,title,url,views=0):
    p=Page.objects.get_or_create(category=cat,title=title,url=url,views=views)
    return p
def add_cat(name,views=0,likes=0):
    c=Category.objects.get_or_create(name=name,views=views,likes=likes)[0]
    return c

if __name__=='__main__':

    print 'Starting rango population script'
    populate()

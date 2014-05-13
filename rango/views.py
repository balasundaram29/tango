from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect
from rango.models import Category,Page,UserProfile
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from datetime import datetime
from rango.bing_search import run_query
def index(request):
    '''if "last_visit" in request.COOKIES:
        return HttpResponse("Your favorite color is %s" % \
            request.COOKIES["last_visit"][:-1])'''
    from datetime import datetime
    dt = datetime.now()
    from django.utils.dateformat import DateFormat
    from django.utils.formats import get_format
    df = DateFormat(dt)
    dfmt=get_format('DATE_FORMAT')
    print 'date format is',dfmt
    ds=df.format(get_format('DATE_FORMAT'))
    print ds
    request.session.set_test_cookie()
    context=RequestContext(request)
    cat_list=get_category_list() #Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]



    #visits=int(request.COOKIES.get('visits','0'))
    if request.session.get('last_visit'):
        #last_visit=request.COOKIES['last_visit']
        #print repr(last_visit[:-7])
        last_visit_time= request.session.get('last_visit')#datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
        visits=request.session.get('visits',0)
        if (datetime.now()-datetime.strptime(last_visit_time[:-7],"%Y-%m-%d %H:%M:%S")).seconds > 5:
            visits=visits+1
            request.session['visits']=visits
            request.session['last_visit']=str(datetime.now())
    else:

        request.session['last_visit']=str(datetime.now())
        request.session['visits']=1
        visits=1
    context_dict={'cat_list':cat_list,'pages':page_list,'visits':visits}
    response= render_to_response('rango/index.html',context_dict,context)
    return response

def about(request):
    context=RequestContext(request)
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

# remember to include the visit data
    return render_to_response('rango/about.html', {'visits': count}, context)


def category(request,category_name_url):
    context=RequestContext(request)
    cat_list=get_category_list()
    category_name=category_name_url.replace('_',' ')
    context_dict={'cat_list':cat_list,'category_name':category_name}
    context_dict['category_name_url']=category_name_url
    try:
        category=Category.objects.get(name=category_name)
        pages=Page.objects.filter(category=category)
        context_dict['pages']=pages
        context_dict['category']=category
    except Category.DoesNotExist:
        pass
    if request.method == 'POST':
        try:
            query=request.POST['query'].strip()
            if query:
                result_list=run_query(query)
                context_dict['result_list']=result_list
        except:
            pass
    return render_to_response('rango/category.html',context_dict,context)

@login_required
def like_category(request):
    context=RequestContext(request)
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    likes=0
    if cat_id:
        category=Category.objects.get(id=int(cat_id))
        if category :
            likes=category.likes+1
            category.likes = likes
            category.save()
    return HttpResponse(likes)

def add_category(request):
    context=RequestContext(request)

    if  not request.user.is_authenticated():
        return  HttpResponseRedirect('/rango/login/')
    if request.method == 'POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form=CategoryForm()
    return render_to_response('rango/add_category.html',{'form':form},context)

def auto_add_page(request):
    context=RequestContext(request)
    cat_id=None
    url=None
    title=None
    context_dict={}
    if request.method== 'GET':
        cat_id=request.GET['category_id']
        url=request.GET['url']
        title=request.GET['title']
        if cat_id:
            category=Category.objects.get(id=int(cat_id))
            p=Page.objects.get_or_create(category=category,title=title,url=url)
            pages=Page.objects.filter(category=category).order_by('-views')
            context_dict['pages']=pages

    return render_to_response('rango/page_list.html',context_dict,context)

def add_page(request,category_name_url):
    if  not request.user.is_authenticated():
        return  HttpResponseRedirect('/rango/login/')
    context=RequestContext(request)
    category_name=decodeURL(category_name_url)
    if request.method=='POST':
        form=PageForm(request.POST)
        if form.is_valid():
            page=form.save(commit=False)
            try:
                cat=Category.objects.get(name=category_name)
                page.category=cat

            except Category.DoesNotExist:
                return render_to_response('rango/add_category',{},context)

            page.views=0
            page.save()
            return category(request,category_name_url)
        else:
            print form.errors
    else:
        form=PageForm()

    return render_to_response('rango/add_page.html',{'category_name_url':category_name_url,'category_name':category_name,'form':form},context)

def register(request):
    if request.session.test_cookie_worked():
        print ">>>> TEST COOKIE WORKED!"
    context=RequestContext(request)
    registered=False
    if request.method == 'POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            if 'picture' in request.FILES:
               profile.picture=request.FILES['picture']
            profile.save()
            registered=True
        else:
            print user_form.errors,profile_form.errors
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render_to_response('rango/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered},context)

def user_login(request):
    context=RequestContext(request)
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
             if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
             else:
                return HttpResponse('Your account has been disabled')
        else:
             print 'Invalid login details :{0},{1}'.format(username,password)
             return HttpResponse('Invalid login details supplied')
    else:
        return render_to_response('rango/login.html',{},context)

@login_required
def restricted(request):
    return HttpResponse('Since you are logged in , you can see this text')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango')

def search(request):
    context=RequestContext(request)
    result_list=[]
    if request.method=='POST':
        query=request.POST['query'].strip()
        if query:
             result_list = run_query(query)

    return render_to_response('rango/search.html',{'result_list':result_list},context)

def profile(request):
    context=RequestContext(request)
    u=User.objects.get(username=request.user)
    profile=UserProfile.objects.get(user=u)
    return render_to_response('rango/profile.html',{'profile':profile},context)

def track_url(request):
    if request.method=='GET':
        if 'page_id' in request.GET :
            page=Page.objects.get(id=request.GET['page_id'])
            try:
                if page:
                    page.views=page.views+1
                    url=page.url
                    page.save()
                else:
                    url='/rango/'
            except:
                url='/rango/'

        else:
            url='/rango'
    return redirect(url)

def get_category_list(max_results=0,starts_with=''):
    cat_list=[]
    if starts_with:
        cat_list=Category.objects.filter(name__istartswith=starts_with)
    else:
        cat_list=Category.objects.all()
    if max_results > 0:
        if len(cat_list) > max_results :
            cat_list = cat_list[:max_results]
    for category in cat_list:
        category.url=encodeURL(category.name)
    return cat_list

def suggest_category(request):
    context=RequestContext(request)
    cat_list=[]
    starts_with= ''
    if request.method=='GET':
        starts_with=request.GET['suggestion']
    cat_list=get_category_list(8,starts_with)
    return render_to_response('rango/category_list.html',{'cat_list':cat_list},context)

def decodeURL(crypticURL):
	return crypticURL.replace('_',' ')

def encodeURL(theURL):
    encoded=theURL.replace(' ','_')
    return encoded

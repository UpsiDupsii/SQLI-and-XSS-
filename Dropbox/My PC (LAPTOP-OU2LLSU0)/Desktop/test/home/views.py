from django.shortcuts import render
from .models import Test
import re 
import csv


path = 'data/csvsspatterns.csv'

# Create your views here.
def index(request):
    
    
    query = request.GET.get("search", default='')
    
    
    queries = (Test.objects.filter(name__icontains=query)) | Test.objects.filter(description__icontains=query)
    context = {
        'queries': queries,
        'search' : query,
        
    }
    if query == '':
        return render (request, 'index.html', context)
    
    
    else:
        pattern = r"""^([']|[`]|[<]|[,]|["]|[/]|[;]|[-]|[%]|[+][|]|[@]|[#]|AND|1-false|1-true|-2|1'|OR|HAVING|ORDER|RLIKE|IF|[(]|[)]|foo|FOO|SLEEP|waitfor|benchmark|AnD|UNION)|(["]|[#]|'1|-|'|[+]|%|@|;|1=1|1=0|x=x|x=y|'%'='|=)$"""
        
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for cell in row:
                    
                    """Below are the two if statements to check 'query' uniquely in two different ways in the csv file"""
                    # if re.search(query, cell) or re.search(pattern, query):
                    if (cell == query) or re.search(pattern, query):
                        return render(request, 'false.html', context)
                
        
            else:
                return render(request, 'index.html', context)
            
    
    
def forms(request):
    
    if request.method=="POST":
        name = request.POST.get('name', default='')
        description = request.POST.get('description', default='')
        context = {
        'searchh': name,
        }
        
        res = description.split(" ")
        print(name, res)
        
        
        
        pattern = r"""^([']|[`]|[<]|[,]|["]|[/]|[;]|[-]|[%]|[+][|]|[@]|[#]|AND|1-false|1-true|-2|1'|OR|HAVING|ORDER|RLIKE|IF|foo|FOO|SLEEP|waitfor|benchmark|AnD|UNION)|(["]|[#]|'1|-|'|[(]|[+]|%|@|;|1=1|1=0|x=x|x=y|'%'='|=)$"""
        
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for cell in row:
                    for i in res:
                        if i != "":
                            
                            """Below are the two if conditions to check csv file uniquely, you can compare both of them"""
                            # if re.search(pattern, i) or re.search(pattern, name) or re.searc(i, cell):
                            if (name == cell) or re.search(pattern, name) or re.search(pattern, i):
                                print(f"Malicious word is {i}")
                                contxt = {
                                    "search": i,
                                }
                                return render(request, 'false.html', contxt)
        
        save_data = Test(name=name, description = description)
        save_data.save()
        
    return render(request, 'form.html')
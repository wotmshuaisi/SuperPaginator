# SuperPaginator

[![forthebadge](http://forthebadge.com/images/badges/built-by-codebabes.svg)](http://forthebadge.com)  

It's easy to used django-paginator to paging some data row,  
but still trouble，need to write some `template language`,  
judgment page count and many more...  
Use that plugin can auto create `bootscrap paging code`, `paged queryset data` and  
`request parameter persistence`.  
This plugin maybe written suck, but it's working for me,  
hope it can work for you.

# Getting Started

Usually i move SuperPaginator into my Django `utils` document,  
to import SuperPaginator you have to create a `__init__.py` file into `utils`.

## How to use

1. build a SuperPaginator object with 

        {QuerySet Data},
        {How much row you wana show on the page},
        {How much html page link you wanna show on the page},
        {Current page count},
        {Http request parameter(QueryDict Object)},
        [Http request parameter string `default is page`, you can change to another]

2. get object's parameter

        object.html  # it's paging html code
        object.limit_data  # it's paged data

## Example

Python Part

```python
from utils.SuperPaginator.paging import SuperPaginator
import copy


def IndexViewer(request):
    current_page = request.GET.get['page']  # get current page number
    param_dict = copy.deepcopy(request.GET)  # deep copy your http request param
    param_dict._mutable = True  # to edit http request param

    queryset_data = models.ExampleModels.objects.filter(age__lte=32)  # get data from models

    paging_obj = SuperPaginator(queryset_data, 10, 5, current_page, param_dict)  # create SuperPaginator object
    
    return render(request, 'Example.html', {
        'paging_html': paging_obj.html,  # bootstrap paging html code
        'data_result': paging_obj.limit_data  # paged queryset data
    })
```

Html Part

```html
<ul>
{% for row in data_result %}
    <li>{{ row }}</li>
{% endfor %}
</ul>
{{ paging_html }}
```

## Depends
- django paginator
- django urlencode

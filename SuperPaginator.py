from django.core.paginator import Paginator


class SuperPaginator:
    def __init__(self, data_list, per_page, show_num, cur_page, request_param, get_str='page'):
        """
        :param data_list: django models data list
        :param per_page: every page show rows
        :param show_num: how much pages link you wanna generat
        :param cur_page: current page from http request param
        :request_param: http request param
        :get_str: http custom param, default is 'page'
        :param obj: paginator object
        :return:
        """
        self.show_num = show_num
        self.cur_page = cur_page
        self.per_page = per_page
        self.data_list = data_list
        self.request_param = request_param
        self.get_str = get_str
        self.obj = Paginator(data_list, self.per_page)
        try:
            self.obj = self.obj.page(self.cur_page)
        except Exception:
            self.obj = self.obj.page(1)

    @property
    def start(self):
        """
        :return: limit start number
        """
        return (self.obj.number - 1) * self.per_page

    @property
    def end(self):
        """
        :return: limit end number
        """
        return self.obj.number * self.per_page

    def request_param_get(self, p):
        """
        reset param 'get_str' to p
        :return: request param urlencode
        """
        self.request_param[self.get_str] = p
        return self.request_param.urlencode()

    @property
    def html(self):
        """
        :start_tag: nav ul html tag str
        :end_tag: nav ul html close tag str
        :previous_page_str: last page html tag str
        :next_page_str: next page html tag str
        :show_pages_str: page html li tag str
        :return: html string with bootstrap
        """

        start_tag = """
        <nav aria-label="Page navigation">
            <ul class="pagination">
        """
        end_tag = """
            </ul>
        </nav>
        """
        show_pages_str = ''

        # prev
        if self.obj.has_previous():  # if has last page then enable last page link
            previous_page_str = '''
                <li>
                    <a href="?{}" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>'''.format(self.request_param_get(self.obj.previous_page_number()))
        else:  # or disabled
            previous_page_str = '''
                <li class="disabled">
                    <a href="" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                    </a>
                </li>'''

        # num
        for page in self.obj.paginator.page_range:  # each erver page number
            # if page in show_num range then show it
            if abs(self.obj.number - page) < self.show_num:
                if self.obj.number == page:  # if number is current page then active it
                    show_pages_str += '''
                        <li class="active">
                            <a href="?{}">{}</a>
                        </li>
                        '''.format(self.request_param_get(page), page)
                    continue
                show_pages_str += '''
                    <li class="">
                        <a href="?{}">{}</a>
                    </li>'''.format(self.request_param_get(page), page)  # add paging link to string

        # next
        if self.obj.has_next():  # if has next page then enable nextpage link
            next_page_str = '''
                <li class="">
                    <a href="?{}" aria-label="Previous">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>'''.format(self.request_param_get(self.obj.next_page_number()))
        else:  # or disabled
            next_page_str = '''
                <li class="disabled">
                    <a href="" aria-label="Previous">
                        <span aria-hidden="true">&raquo;</span>
                    </a>
                </li>'''

        return "{}{}{}{}{}".format(
            start_tag,
            previous_page_str,
            show_pages_str,
            next_page_str,
            end_tag)  # format all string to create bootstrap html code

    @property
    def limit_data(self):
        """
        :return: django queryset data with limit
        """
        return self.data_list[self.start:self.end]

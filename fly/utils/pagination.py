from django.http import QueryDict
from urllib.parse import urlencode
from django.utils.safestring import mark_safe


def _create_page_link(params, page_number, text, active=False, disabled=False):
    params['page'] = page_number
    css_classes = ['page-item']
    if active:
        css_classes.append('active')
    if disabled:
        css_classes.append('disabled')

    link_template = '<li class="{}"><a class="page-link" href="?{}">{}</a></li>'
    return link_template.format(' '.join(css_classes), urlencode(params, doseq=True), text)


class Pagination(object):

    def __init__(self, request, queryset, page_param='page', page_size=15, plus=5):
        self.request = request
        page = request.GET.get(page_param, "1")
        self.page = int(page) if page.isdecimal() else 1
        self.page_size = page_size
        self.plus = plus
        self.total_count = queryset.count()
        self.page_queryset = queryset[self.start:self.end]

    @property
    def start(self):
        return (self.page - 1) * self.page_size

    @property
    def end(self):
        return self.page * self.page_size

    def get_hidden_inputs(self):
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        return ''.join(f'<input type="hidden" name="{key}" value="{value}">' for key in params for value in params for value in params.getlist(key))

    def page_html(self):
        if not self.total_count:
            return ""

        total_page_count, div = divmod(self.total_count, self.page_size)
        total_page_count += bool(div)  # 如果有余数，增加一页

        if self.page > total_page_count:
            self.page = total_page_count

        half_plus = self.plus // 2
        start_page = max(1, self.page - half_plus)
        end_page = min(total_page_count, self.page + half_plus)

        if total_page_count <= 2 * self.plus + 1:
            start_page, end_page = 1, total_page_count

        params = self.request.GET.copy()  # 复制请求参数

        page_html_list = [
            '<small class="d-flex align-items-center me-3">共 {} 条数据，每页 {} 条，共 {} 页</small>'.format(self.total_count, self.page_size, total_page_count),
            _create_page_link(params,1,'首页'),
            _create_page_link(params, self.page - 1, '&laquo;', disabled=self.page <= 1),
        ]

        for i in range(start_page, end_page + 1):
            page_html_list.append(_create_page_link(params, i, str(i), active=i == self.page))

        page_html_list.extend([
            _create_page_link(params, self.page + 1, '&raquo;', disabled=self.page >= total_page_count),
            _create_page_link(params, total_page_count, '尾页'),
            self._create_search_form(),
        ])

        return mark_safe("".join(page_html_list))

    def _create_search_form(self):
        hidden_inputs = self.get_hidden_inputs()
        return '''
            <li>
                <form style="float: left; margin-left: -1px" method="get">{}
                    <div class="input-group" style="width: 200px">
                        <div class="d-inline-flex">
                            <input type="text" name="page" class="form-control form-control-sm" placeholder="页码" style="width: 60px; height: 30px;">
                            <button class="btn btn-sm" type="submit">跳转</button>
                        </div>
                    </div>
                </form>
            </li>
        '''.format(hidden_inputs)
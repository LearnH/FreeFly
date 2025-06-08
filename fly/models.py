from django.db import models

# 运行基地
class OperatingBase(models.Model):
    name = models.CharField(max_length=100, verbose_name='名称', unique=True)
    base_type_choices = (
        (1,'主运行基地'),
        (2,'辅助运行基地'),
    )
    base_type = models.SmallIntegerField(verbose_name='基地类型', choices=base_type_choices, null=True, blank=True)
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE, verbose_name='运行机场', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    in_charge = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name='负责人', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='电话', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    status_choices = (
        (1, '启用'),
        (2, '停用'),
    )
    status = models.SmallIntegerField(verbose_name='状态', default=1, choices=status_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '运行基地'
        verbose_name_plural = '运行基地'

    def __str__(self):
        return self.name
# 机场
class Airport(models.Model):
    name = models.CharField(max_length=100, verbose_name='机场名称', null=False, blank=False, unique=True)
    icao_code = models.CharField(max_length=4, verbose_name='ICAO代码', null=True, blank=True, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='纬度', null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='经度', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    is_owner = models.BooleanField(default=False, verbose_name='是否本企业机场')
    is_air_harbor = models.BooleanField(default=False, verbose_name='是否水上机场')
    is_temporary = models.BooleanField(default=False, verbose_name='是否临时站点')
    is_tower = models.BooleanField(default=False, verbose_name='是否塔台机场')
    status_choices = (
        (1, '启用'),
        (2, '停用')
    )
    status = models.SmallIntegerField(verbose_name='状态', null=False, blank=False, default=1, choices=status_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '机场'
        verbose_name_plural = '机场'

    def __str__(self):
        return self.name

# 公司
class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='公司名称', null=False, blank=False, unique=True)
    name_en = models.CharField(max_length=4, verbose_name='外文名称', null=True, blank=True, unique=True)
    name_short = models.CharField(max_length=4, verbose_name='简称', null=True, blank=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='上级公司', null=True, blank=True)
    found_time = models.DateField(verbose_name='成立时间', null=True, blank=True)
    legal_person = models.CharField(max_length=100, verbose_name='法人', null=True, blank=True)
    business_scope = models.TextField(verbose_name='经营范围', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='地址', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='电话', null=True, blank=True)
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    website = models.URLField(verbose_name='网站', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    status_choices = (
        (1, '启用'),
        (2, '停用')
    )
    status = models.SmallIntegerField(verbose_name='状态', null=False, blank=False, default=1, choices=status_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '公司'
        verbose_name_plural = '公司'
    def __str__(self):
        return self.name
# 部门
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='部门名称', null=False, blank=False, unique=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='上级部门', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    status_choices = (
        (1, '启用'),
        (2, '停用')
    )
    status = models.SmallIntegerField(verbose_name='状态', null=False, blank=False, default=1, choices=status_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name
# 职位
class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='职位名称', null=False, blank=False, unique=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='所属部门', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    status_choices = (
        (1, '启用'),
        (2, '停用')
    )
    status = models.SmallIntegerField(verbose_name='状态', null=False, blank=False, default=1, choices=status_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '职位'
        verbose_name_plural = '职位'

    def __str__(self):
        return self.name
# 员工
class Employee(models.Model):
    emp_code = models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name='员工编号')
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='姓名')
    photo = models.ImageField(verbose_name='照片', null=True, blank=True)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)
    nationality = models.CharField(max_length=10, null=True, blank=True, verbose_name='国籍')
    ID_type = models.CharField(max_length=10, blank=True, verbose_name='证件类型')
    ID_number = models.CharField(max_length=20, blank=True, verbose_name='证件号')
    birth_date = models.DateField(blank=True, null=True, verbose_name='出生日期')
    nation = models.CharField(max_length=100, blank=True, verbose_name='民族')
    native_place = models.CharField(max_length=100, blank=True, verbose_name='籍贯')
    address = models.CharField(max_length=200, blank=True, verbose_name='通讯地址')
    phone = models.CharField(max_length=20, verbose_name='手机号', null=True, blank=True)
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    political_status = models.CharField(max_length=10, blank=True, verbose_name='政治面貌')
    marital_status_choices = (
        (1, '已婚'),
        (2, '未婚'),
        (3, '离异'),
        (4, '丧偶'),
    )
    marital_status = models.SmallIntegerField(verbose_name='婚姻状况', choices=marital_status_choices, null=True, blank=True)
    education_level_choices = (
        (1, '小学'),
        (2, '初中'),
        (3, '高中'),
        (4, '大专'),
        (5, '本科'),
        (6, '硕士'),
        (7, '博士'),
    )
    education_level = models.SmallIntegerField(verbose_name='教育程度', choices=education_level_choices, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name='紧急联系人姓名')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name='紧急联系人电话')
    emergency_contact_relationship_choices = (
        (1, '父母'),
        (2, '祖父母'),
        (3, '兄弟姐妹'),
        (4, '配偶'),
        (5, '其他'),
    )
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, verbose_name='紧急联系人关系')
    ope_base = models.ForeignKey('OperatingBase', on_delete=models.CASCADE, verbose_name='所属基地', null=True, blank=True)
    employment_type_choices = (
        (1, '全职'),
        (2, '兼职'),
        (3, '实习'),
        (4, '临时'),
    )
    employment_type = models.SmallIntegerField(verbose_name='入职类型', choices=employment_type_choices, default=1)
    employment_date = models.DateField(blank=True, null=True, verbose_name='入职日期')
    confirmable_date = models.DateField(blank=True, null=True, verbose_name='转正日期')
    position = models.ForeignKey('Position', on_delete=models.CASCADE, verbose_name='职位', null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='所属部门', null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True, blank=True)
    is_coach = models.BooleanField(default=False, verbose_name='是否教员')
    status_choices = (
        (1, '在职'),
        (2, '离职'),
    )
    status = models.SmallIntegerField(verbose_name='状态', null=False, blank=False, default=1)
    termination_date = models.DateField(blank=True, null=True, verbose_name='离职日期')
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    # created_user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='创建人', null=True, blank=True, related_name='created_employees')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # updated_user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='更新人', null=True, blank=True, related_name='updated_employees')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'
    def __str__(self):
        return self.name
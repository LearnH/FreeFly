import uuid

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

# 人员
class Person(models.Model):
    person_type_choices = (
        ('employee', '员工'),
        ('student', '学员'),
    )
    person_type = models.CharField(max_length=10, verbose_name='人员类型', choices=person_type_choices, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='姓名')
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=1)
    nationality = models.CharField(max_length=10, null=True, blank=True, verbose_name='国籍')
    ID_type = models.CharField(max_length=10, null=True, blank=True, verbose_name='证件类型')
    ID_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='证件号')
    birth_date = models.DateField(blank=True, null=True, verbose_name='出生日期')
    political_status = models.CharField(max_length=10, null=True, blank=True, verbose_name='政治面貌')
    nation = models.CharField(max_length=100, null=True, blank=True, verbose_name='民族')
    native_place = models.CharField(max_length=100, null=True, blank=True, verbose_name='籍贯')
    phone = models.CharField(max_length=20, verbose_name='手机号', null=True, blank=True)
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='通讯地址')
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
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='紧急联系人姓名')
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='紧急联系人电话')
    emergency_contact_relationship_choices = (
        (1, '父母'),
        (2, '祖父母'),
        (3, '兄弟姐妹'),
        (4, '配偶'),
        (5, '其他'),
    )
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True, verbose_name='紧急联系人关系', choices=emergency_contact_relationship_choices)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    # created_user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='创建人', null=True, blank=True, related_name='created_employees')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # updated_user = models.ForeignKey('User', on_delete=models.SET_NULL, verbose_name='更新人', null=True, blank=True, related_name='updated_employees')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def save(self, *args, **kwargs):
        if not self.pk:  # 只在创建时设置
            self.person_type = self.__class__.__name__.lower()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = '人员'
        verbose_name_plural = '人员'
    def __str__(self):
        return self.name
# 员工
def get_emp_photo_path(instance, filename):
    ext = filename.split('.')[-1]  # 获取文件扩展名
    if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
        ext = 'jpg'  # 默认使用 jpg 格式
    return f'photos/emp_{instance.emp_code}_{uuid.uuid4().hex}.{ext}'
class Employee(Person):
    emp_code = models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name='员工编号')
    photo = models.ImageField(upload_to=get_emp_photo_path, verbose_name='照片', null=True, blank=True)
    marital_status_choices = (
        (1, '已婚'),
        (2, '未婚'),
        (3, '离异'),
        (4, '丧偶'),
    )
    marital_status = models.SmallIntegerField(verbose_name='婚姻状况', choices=marital_status_choices, null=True, blank=True)
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

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = '员工'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.person_type = 'employee'  # 自动设置为员工类型
        super().save(*args, **kwargs)

# 学员
def get_stu_photo_path(instance, filename):
    ext = filename.split('.')[-1]  # 获取文件扩展名
    if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
        ext = 'jpg'  # 默认使用 jpg 格式
    return f'photos/stu_{instance.emp_code}_{uuid.uuid4().hex}.{ext}'
class Student(Person):
    stu_code = models.CharField(max_length=10, null=False, blank=False, unique=True, verbose_name='学员编号')
    photo = models.ImageField(upload_to=get_emp_photo_path, verbose_name='照片', null=True, blank=True)
    ope_base = models.ForeignKey('OperatingBase', on_delete=models.CASCADE, verbose_name='训练基地', null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='训练单位', null=True, blank=True)
    student_type_choices = (
        (1, '本校教员'),
        (2, '整体课程'),
        (3, '分体课程'),
        (4, '熟练检查'),
        (5, '商用补时'),
        (6, '外籍换照'),
        (7, '实践考试'),
        (99, '其他'),
    )
    student_type = models.SmallIntegerField(verbose_name='学员类型', choices=student_type_choices, default=1)
    enter_date = models.DateField(blank=True, null=True, verbose_name='入校日期')
    registration_date = models.DateField(blank=True, null=True, verbose_name='注册日期')
    is_temporary = models.BooleanField(default=False, verbose_name='是否临时')
    status_choices = (
        (1, '在学'),
        (2, '退学'),
        (3, '毕业'),
    )
    status = models.SmallIntegerField(verbose_name='学籍状态', null=False, blank=False, default=1)
    termination_date = models.DateField(blank=True, null=True, verbose_name='毕业/退学日期')

    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.person_type = 'student'  # 自动设置为学员类型
        super().save(*args, **kwargs)

#  机型
class AircraftType(models.Model):
    name = models.CharField(max_length=100, verbose_name='机型名称', null=False, blank=False, unique=True)
    manufacturer = models.CharField(max_length=100, verbose_name='生产厂商', null=True, blank=True)
    aircraft_nature_choices = (
        (1, '单发陆地'),
        (2, '多发陆地'),
    )
    aircraft_nature = models.SmallIntegerField(verbose_name='机型性质', choices=aircraft_nature_choices, default=1)
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
        verbose_name = '机型'
        verbose_name_plural = '机型'
    def __str__(self):
        return self.name
# 航空器
def get_aircraft_file_path(instance, filename):
    ext = filename.split('.')[-1]  # 获取文件扩展名
    return f'certificates/air_{instance.name}_{uuid.uuid4().hex}.{ext}'
class Aircraft(models.Model):
    name = models.CharField(max_length=100, verbose_name='机号', unique=True)
    aircraft_type = models.ForeignKey('AircraftType', on_delete=models.CASCADE, verbose_name='机型', null=True, blank=True)
    introduction_date = models.DateField(blank=True, null=True, verbose_name='引进日期')
    device_type_choices = (
        (1, '真机'),
        (2, '训练器'),
        (3, '模拟机'),
    )
    device_type = models.SmallIntegerField(verbose_name='设备类型', choices=device_type_choices, default=1)
    status_choices = (
        (1, '适航'),
        (2, '待检'),
        (3, '定检中'),
        (4, '大修'),
        (5, '损伤'),
        (6, '损毁'),
        (99, '停用')
    )
    status = models.SmallIntegerField(verbose_name='状态', default=1, choices=status_choices)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, verbose_name='所属公司', null=True, blank=True)
    ope_base = models.ForeignKey('OperatingBase', on_delete=models.CASCADE, verbose_name='运行基地', null=True, blank=True)
    airworthiness_certificate = models.FileField(upload_to=get_aircraft_file_path, verbose_name='适航证', null=True, blank=True)
    radio_station_license = models.FileField(upload_to=get_aircraft_file_path, verbose_name='电台执照', null=True, blank=True)
    registration_certificate = models.FileField(upload_to=get_aircraft_file_path, verbose_name='国籍登记证', null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Mate:
        verbose_name = '航空器'
        verbose_name_plural = '航空器'
    def __str__(self):
        return self.name
# 飞行课程
class FlightCourse(models.Model):
    name = models.CharField(max_length=100, verbose_name='课程名称', null=False, blank=False, unique=True)
    device_type = models.SmallIntegerField(verbose_name='设备类型', choices=Aircraft.device_type_choices, default=1)
    aircraft_nature = models.SmallIntegerField(verbose_name='机型性质', choices=AircraftType.aircraft_nature_choices, default=1)
    field_transition_choices = (
        (1, '本场'),
        (2, '转场'),
    )
    field_transition = models.SmallIntegerField(verbose_name='本转性质', default=1, choices=field_transition_choices)
    fly_nature_choices = (
        (1, '带飞'),
        (2, '单飞'),
        (3, '机长'),
        (4, '副驾驶'),
    )
    fly_nature = models.SmallIntegerField(verbose_name='飞行性质', choices=fly_nature_choices, null=True, blank=True)
    day_night_choices = (
        (1, '昼间'),
        (2, '夜间'),
        (3, '跨昼夜'),
    )
    day_night = models.SmallIntegerField(verbose_name='昼夜性质', default=1, choices=day_night_choices)
    fly_category_choices = (
        (1, '飞行娱乐'),
        (2, '飞行训练'),
        (3, '阶段检查'),
        (4, '实践考试'),
        (5, '任教检查'),
        (6, '熟练检查'),
        (7, '单飞'),
        (8, '螺旋'),
        (99, '其他'),
    )
    fly_category = models.SmallIntegerField(verbose_name='飞行种类', choices=fly_category_choices, default=2)
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
        verbose_name = '飞行课程'
        verbose_name_plural = '飞行课程'
    def __str__(self):
        return self.name
# 飞行记录
class FlightRecord(models.Model):
    flight_date = models.DateField(verbose_name='飞行日期')
    task_pilot = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='task_records', verbose_name='任务飞行员')
    flight_course = models.ForeignKey('FlightCourse', on_delete=models.CASCADE, verbose_name='飞行课程')
    field_transition_choices = (
        (1, '本场'),
        (2, '转场'),
    )
    field_transition = models.SmallIntegerField(verbose_name='本转性质', default=1, choices=field_transition_choices)
    fly_nature_choices = (
        (1, '带飞'),
        (2, '单飞'),
        (3, '机长'),
        (4, '副驾驶'),
    )
    fly_nature = models.SmallIntegerField(verbose_name='飞行性质', choices=fly_nature_choices, null=True, blank=True)
    day_night_choices = (
        (1, '昼间'),
        (2, '夜间'),
        (3, '跨昼夜'),
    )
    day_night = models.SmallIntegerField(verbose_name='昼夜性质', default=1, choices=day_night_choices)
    fly_category = models.SmallIntegerField(verbose_name='飞行种类', choices=FlightCourse.fly_category_choices, null=True, blank=True)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE, verbose_name='航空器')
    aircraft_type = models.ForeignKey('AircraftType', on_delete=models.CASCADE, verbose_name='机型')
    departure_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departure_records', verbose_name='出发机场', null=True, blank=True)
    arrival_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arrival_records', verbose_name='到达机场', null=True, blank=True)
    open_time = models.TimeField(verbose_name='开车时间')
    take_off_time = models.TimeField(verbose_name='起飞时间', null=True, blank=True)
    landing_time = models.TimeField(verbose_name='落地时间', null=True, blank=True)
    close_time = models.TimeField(verbose_name='关车时间')
    left_seat_person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name='左座人员', related_name='left_seat_person', null=True, blank=True)
    right_seat_person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name='右座人员', related_name='right_seat_person', null=True, blank=True)
    flight_duration = models.SmallIntegerField(verbose_name='飞行时长')
    flight_sortie = models.SmallIntegerField(verbose_name='起落架次',blank=True, null=True)
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '飞行记录'
        verbose_name_plural = '飞行记录'
    def __str__(self):
        return f"{self.task_pilot.name} - {self.flight_course.name} - {self.flight_date}"

    @property
    def flight_duration_display(self):
        if self.flight_duration is None:
            return ''
        hours, remainder = divmod(self.flight_duration, 60)
        return f"{hours:02d}:{remainder:02d}"
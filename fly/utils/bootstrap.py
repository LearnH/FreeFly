from django import forms

class BaseModelForm(forms.ModelForm):
    """
        基础 ModelForm 父类，包含通用的字段样式和属性设置
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 为所有字段设置适当的类
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

            # 添加placeholder
            if field.label and not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['placeholder'] = field.label

            # 处理必填字段
            if field.required:
                field.widget.attrs['required'] = 'required'

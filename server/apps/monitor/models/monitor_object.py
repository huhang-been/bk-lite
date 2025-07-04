from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo


class MonitorObject(TimeInfo, MaintainerInfo):
    LEVEL_CHOICES = [('base', 'Base'), ('derivative', 'Derivative')]

    name = models.CharField(unique=True, max_length=100, verbose_name='监控对象')
    icon = models.CharField(max_length=100, default="", verbose_name='监控对象图标')
    type = models.CharField(max_length=50, verbose_name='监控对象类型')
    level = models.CharField(default="base", max_length=50, verbose_name='监控对象级别')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父级监控对象')
    description = models.TextField(blank=True, verbose_name='监控对象描述')
    default_metric = models.TextField(blank=True, verbose_name='默认指标')
    instance_id_keys = models.JSONField(default=list, verbose_name='联合唯一实例ID键列表')
    supplementary_indicators = models.JSONField(default=list, verbose_name='对象实例补充指标')

    class Meta:
        verbose_name = '监控对象'
        verbose_name_plural = '监控对象'


class MonitorInstance(TimeInfo, MaintainerInfo):
    id = models.CharField(primary_key=True, max_length=200, verbose_name='监控对象实例ID')
    name = models.CharField(db_index=True, max_length=200, default="", verbose_name='监控对象实例名称')
    interval = models.IntegerField(default=10, verbose_name='监控实例采集间隔(s)')
    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='监控对象')
    auto = models.BooleanField(default=False, verbose_name='是否自动发现')
    is_deleted = models.BooleanField(db_index=True, default=False, verbose_name='是否删除')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = '监控对象实例'
        verbose_name_plural = '监控对象实例'


class MonitorInstanceOrganization(TimeInfo, MaintainerInfo):
    monitor_instance = models.ForeignKey(MonitorInstance, on_delete=models.CASCADE, verbose_name='监控对象实例')
    organization = models.CharField(max_length=100, verbose_name='组织id')

    class Meta:
        verbose_name = '监控对象实例组织'
        verbose_name_plural = '监控对象实例组织'
        unique_together = ('monitor_instance', 'organization')


class MonitorObjectOrganizationRule(TimeInfo, MaintainerInfo):
    monitor_object = models.ForeignKey(MonitorObject, on_delete=models.CASCADE, verbose_name='监控对象')
    name = models.CharField(max_length=100, verbose_name='分组规则名称')
    organizations = models.JSONField(default=list, verbose_name='所属组织')
    rule = models.JSONField(default=dict, verbose_name='分组规则详情')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
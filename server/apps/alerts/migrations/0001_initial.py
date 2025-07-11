# Generated by Django 4.2.7 on 2025-06-25 09:52

import apps.alerts.utils.util
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AggregationRules",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("rule_id", models.CharField(db_index=True, help_text="规则ID", max_length=100, unique=True)),
                ("name", models.CharField(help_text="规则名称", max_length=100)),
                ("description", models.TextField(blank=True, help_text="规则描述", null=True)),
                ("is_active", models.BooleanField(db_index=True, default=True, help_text="是否启用")),
                ("template_title", models.CharField(blank=True, help_text="模板标题", max_length=200, null=True)),
                ("template_content", models.TextField(blank=True, help_text="模板内容", null=True)),
                ("severity", models.CharField(default="warning", help_text="严重程度", max_length=32)),
                ("condition", models.JSONField(default=list, help_text="规则条件配置")),
                (
                    "type",
                    models.CharField(
                        choices=[("alert", "告警"), ("incident", "事故")], default="alert", help_text="聚合类型", max_length=32
                    ),
                ),
            ],
            options={"verbose_name": "聚合规则", "verbose_name_plural": "聚合规则", "db_table": "alerts_aggregation_rules",},
        ),
        migrations.CreateModel(
            name="Alert",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("alert_id", models.CharField(db_index=True, help_text="告警ID", max_length=100, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "待响应"),
                            ("processing", "处理中"),
                            ("resolved", "已处理"),
                            ("closed", "已关闭"),
                            ("unassigned", "未分派"),
                        ],
                        db_index=True,
                        default="unassigned",
                        help_text="告警状态",
                        max_length=32,
                    ),
                ),
                ("level", models.CharField(db_index=True, help_text="级别", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, help_text="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True, help_text="更新时间")),
                ("title", models.CharField(help_text="标题", max_length=200)),
                ("content", models.TextField(help_text="内容")),
                ("labels", models.JSONField(default=dict, help_text="标签")),
                ("first_event_time", models.DateTimeField(blank=True, help_text="首次事件时间", null=True)),
                ("last_event_time", models.DateTimeField(blank=True, help_text="最近事件时间", null=True)),
                ("item", models.CharField(blank=True, db_index=True, help_text="事件指标", max_length=128, null=True)),
                (
                    "resource_id",
                    models.CharField(blank=True, db_index=True, help_text="资源唯一ID", max_length=128, null=True),
                ),
                ("resource_name", models.CharField(blank=True, help_text="资源名称", max_length=128, null=True)),
                ("resource_type", models.CharField(blank=True, help_text="资源类型", max_length=64, null=True)),
                (
                    "operate",
                    models.CharField(
                        blank=True,
                        choices=[("acknowledge", "认领"), ("close", "关闭"), ("reassign", "转派"), ("assign", "分派")],
                        help_text="告警操作",
                        max_length=64,
                        null=True,
                    ),
                ),
                ("operator", models.JSONField(blank=True, default=list, help_text="告警处理人")),
                ("source_name", models.CharField(blank=True, help_text="告警源名称", max_length=100, null=True)),
                ("fingerprint", models.CharField(db_index=True, help_text="告警指纹", max_length=32)),
                ("rule_id", models.CharField(blank=True, help_text="触发该事件的规则ID", max_length=256, null=True)),
            ],
            options={"db_table": "alerts_alert", "ordering": ["-updated_at"],},
        ),
        migrations.CreateModel(
            name="AlertAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("name", models.CharField(help_text="分派策略名称", max_length=200, unique=True)),
                (
                    "match_type",
                    models.CharField(choices=[("all", "全部匹配"), ("filter", "过滤匹配")], help_text="匹配类型", max_length=32),
                ),
                ("match_rules", models.JSONField(default=list, help_text="匹配规则")),
                ("personnel", models.JSONField(blank=True, default=list, help_text="分派人员", null=True)),
                ("notify_channels", models.JSONField(default=list, help_text="通知渠道")),
                ("notification_scenario", models.JSONField(default=list, help_text="通知场景")),
                ("config", models.JSONField(default=dict, help_text="分派配置")),
                ("notification_frequency", models.JSONField(blank=True, default=dict, help_text="通知频率配置", null=True)),
                ("is_active", models.BooleanField(db_index=True, default=True, help_text="是否启用")),
            ],
            options={"db_table": "alerts_alert_assignment",},
        ),
        migrations.CreateModel(
            name="AlertShield",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("name", models.CharField(help_text="屏蔽策略名称", max_length=200, unique=True)),
                (
                    "match_type",
                    models.CharField(choices=[("all", "全部匹配"), ("filter", "过滤匹配")], help_text="匹配类型", max_length=32),
                ),
                ("match_rules", models.JSONField(default=list, help_text="匹配规则")),
                ("suppression_time", models.JSONField(default=dict, help_text="屏蔽时间配置")),
                ("is_active", models.BooleanField(db_index=True, default=True, help_text="是否启用")),
            ],
            options={"db_table": "alerts_alert_shield",},
        ),
        migrations.CreateModel(
            name="AlertSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("name", models.CharField(help_text="告警源名称", max_length=100)),
                ("source_id", models.CharField(db_index=True, help_text="告警源ID", max_length=100, unique=True)),
                (
                    "source_type",
                    models.CharField(
                        choices=[
                            ("prometheus", "Prometheus"),
                            ("zabbix", "Zabbix"),
                            ("webhook", "Webhook"),
                            ("log", "日志"),
                            ("monitor", "监控"),
                            ("cloud", "云监控"),
                            ("nats", "NATS"),
                            ("restful", "RESTFul"),
                        ],
                        help_text="告警源类型",
                        max_length=20,
                    ),
                ),
                ("config", models.JSONField(default=dict, help_text="告警源配置")),
                (
                    "secret",
                    models.CharField(default=apps.alerts.utils.util.gen_app_secret, max_length=100, verbose_name="密钥"),
                ),
                ("logo", models.TextField(blank=True, help_text="告警源logo", null=True)),
                (
                    "access_type",
                    models.CharField(
                        choices=[("built_in", "内置"), ("customize", "自定义")],
                        default="built_in",
                        help_text="告警源接入类型",
                        max_length=64,
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True, help_text="是否启用")),
                ("is_effective", models.BooleanField(default=True, help_text="是否生效")),
                ("description", models.TextField(blank=True, help_text="告警源描述", null=True)),
                ("last_active_time", models.DateTimeField(blank=True, help_text="最近活跃时间", null=True)),
                ("is_delete", models.BooleanField(db_index=True, default=False, help_text="是否删除")),
            ],
            managers=[("all_objects", django.db.models.manager.Manager()),],
        ),
        migrations.CreateModel(
            name="CorrelationRules",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created Time")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated Time")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("name", models.CharField(help_text="关联规则名称", max_length=100, unique=True)),
                (
                    "scope",
                    models.CharField(choices=[("all", "全部匹配"), ("filter", "过滤匹配")], help_text="作用范围", max_length=20),
                ),
                (
                    "rule_type",
                    models.CharField(choices=[("alert", "告警"), ("event", "事件")], help_text="规则类型", max_length=20),
                ),
                ("description", models.TextField(blank=True, null=True, verbose_name="描述")),
            ],
            options={"verbose_name": "关联规则", "verbose_name_plural": "关联规则", "db_table": "alerts_correlation_rules",},
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("raw_data", models.JSONField(help_text="原始数据")),
                ("received_at", models.DateTimeField(auto_now_add=True, db_index=True, help_text="接收时间")),
                ("title", models.CharField(help_text="事件标题", max_length=200)),
                ("description", models.TextField(blank=True, help_text="事件描述", null=True)),
                ("level", models.CharField(db_index=True, help_text="级别", max_length=32)),
                ("start_time", models.DateTimeField(db_index=True, help_text="事件开始时间")),
                ("end_time", models.DateTimeField(blank=True, db_index=True, help_text="事件结束时间", null=True)),
                ("labels", models.JSONField(default=dict, help_text="事件元数据")),
                (
                    "action",
                    models.CharField(
                        choices=[("created", "产生"), ("closed", "关闭")],
                        default="created",
                        help_text="事件动作",
                        max_length=32,
                    ),
                ),
                ("rule_id", models.CharField(blank=True, help_text="触发该事件的规则ID", max_length=100, null=True)),
                ("event_id", models.CharField(db_index=True, help_text="事件唯一ID", max_length=100, unique=True)),
                ("external_id", models.CharField(blank=True, help_text="外部事件ID", max_length=128, null=True)),
                ("item", models.CharField(blank=True, db_index=True, help_text="事件指标", max_length=128, null=True)),
                (
                    "resource_id",
                    models.CharField(blank=True, db_index=True, help_text="资源唯一ID", max_length=64, null=True),
                ),
                ("resource_type", models.CharField(blank=True, help_text="资源类型", max_length=64, null=True)),
                ("resource_name", models.CharField(blank=True, help_text="资源名称", max_length=128, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "待响应"),
                            ("processing", "处理中"),
                            ("resolved", "已处理"),
                            ("closed", "已关闭"),
                            ("shield", "已屏蔽"),
                            ("received", "已接收"),
                        ],
                        default="received",
                        help_text="事件状态",
                        max_length=32,
                    ),
                ),
                ("assignee", models.JSONField(blank=True, default=list, help_text="事件责任人")),
                ("value", models.FloatField(blank=True, null=True, verbose_name="事件值")),
            ],
            options={"db_table": "alerts_event", "ordering": ["-received_at"],},
        ),
        migrations.CreateModel(
            name="Incident",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_by", models.CharField(default="", max_length=32, verbose_name="Creator")),
                ("updated_by", models.CharField(default="", max_length=32, verbose_name="Updater")),
                ("domain", models.CharField(default="domain.com", max_length=100, verbose_name="Domain")),
                (
                    "updated_by_domain",
                    models.CharField(default="domain.com", max_length=100, verbose_name="updated by domain"),
                ),
                ("incident_id", models.CharField(db_index=True, help_text="事故ID", max_length=100, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "待响应"), ("processing", "处理中"), ("resolved", "已处理"), ("closed", "已关闭")],
                        db_index=True,
                        default="pending",
                        help_text="事件状态",
                        max_length=32,
                    ),
                ),
                ("level", models.CharField(db_index=True, help_text="级别", max_length=32)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, help_text="创建时间")),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True, help_text="更新时间")),
                ("title", models.CharField(help_text="标题", max_length=256)),
                ("content", models.TextField(blank=True, help_text="内容", null=True)),
                ("note", models.TextField(blank=True, help_text="事件备注", null=True)),
                ("labels", models.JSONField(default=dict, help_text="标签")),
                (
                    "operate",
                    models.CharField(
                        blank=True,
                        choices=[("acknowledge", "认领"), ("close", "关闭"), ("reassign", "转派"), ("assign", "分派")],
                        help_text="操作",
                        max_length=64,
                        null=True,
                    ),
                ),
                ("operator", models.JSONField(blank=True, default=list, help_text="处理人")),
                (
                    "fingerprint",
                    models.CharField(blank=True, db_index=True, help_text="事件指纹", max_length=32, null=True),
                ),
            ],
            options={"db_table": "alerts_incident",},
        ),
        migrations.CreateModel(
            name="Level",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("level_id", models.SmallIntegerField(help_text="级别ID")),
                ("level_name", models.CharField(help_text="级别名称", max_length=32)),
                ("level_display_name", models.CharField(help_text="级别中文名称", max_length=32)),
                ("color", models.CharField(blank=True, help_text="颜色代码", max_length=16, null=True)),
                ("icon", models.TextField(blank=True, help_text="图标base64", null=True)),
                ("description", models.CharField(blank=True, help_text="级别描述", max_length=300, null=True)),
                (
                    "level_type",
                    models.CharField(
                        choices=[("event", "事件"), ("alert", "告警"), ("incident", "事故")], help_text="级别类型", max_length=32
                    ),
                ),
                ("built_in", models.BooleanField(default=False, help_text="是否为内置级别")),
            ],
            options={"db_table": "alerts_level",},
        ),
        migrations.CreateModel(
            name="AlertReminderTask",
            fields=[
                (
                    "alert",
                    models.OneToOneField(
                        help_text="关联的告警",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="alerts.alert",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, help_text="是否激活")),
                ("reminder_count", models.IntegerField(default=0, help_text="已提醒次数")),
                ("current_frequency_minutes", models.IntegerField(help_text="当前提醒频率(分钟)")),
                ("current_max_reminders", models.IntegerField(help_text="当前最大提醒次数")),
                ("next_reminder_time", models.DateTimeField(help_text="下次提醒时间")),
                ("last_reminder_time", models.DateTimeField(blank=True, help_text="上次提醒时间", null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "alerts_reminder_task",},
        ),
        migrations.AddConstraint(
            model_name="level",
            constraint=models.UniqueConstraint(fields=("level_id", "level_type"), name="unique_level_id_level_type"),
        ),
        migrations.AddField(model_name="incident", name="alert", field=models.ManyToManyField(to="alerts.alert"),),
        migrations.AddField(
            model_name="event",
            name="source",
            field=models.ForeignKey(
                help_text="告警源", on_delete=django.db.models.deletion.CASCADE, to="alerts.alertsource"
            ),
        ),
        migrations.AddField(
            model_name="correlationrules",
            name="aggregation_rules",
            field=models.ManyToManyField(
                help_text="关联的聚合规则", related_name="correlation_rules", to="alerts.aggregationrules"
            ),
        ),
        migrations.AddIndex(
            model_name="alertsource",
            index=models.Index(fields=["name", "source_type"], name="alerts_aler_name_8938e7_idx"),
        ),
        migrations.AddField(model_name="alert", name="events", field=models.ManyToManyField(to="alerts.event"),),
        migrations.AddIndex(
            model_name="incident",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["created_at"], name="incident_created_btree"),
        ),
        migrations.AddIndex(
            model_name="incident",
            index=django.contrib.postgres.indexes.GinIndex(fields=["operator"], name="incident_operator_gin"),
        ),
        migrations.AddIndex(
            model_name="event",
            index=models.Index(fields=["source", "received_at"], name="alerts_even_source__4b038c_idx"),
        ),
        migrations.AddIndex(
            model_name="event",
            index=django.contrib.postgres.indexes.GinIndex(fields=["labels"], name="event_labels_gin"),
        ),
        migrations.AddField(
            model_name="alertremindertask",
            name="assignment",
            field=models.ForeignKey(
                help_text="分派策略", on_delete=django.db.models.deletion.CASCADE, to="alerts.alertassignment"
            ),
        ),
        migrations.AddIndex(
            model_name="alert", index=models.Index(fields=["status", "level"], name="alert_status_level_idx"),
        ),
        migrations.AddIndex(
            model_name="alert",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["created_at"], name="alert_created_btree"),
        ),
        migrations.AddIndex(
            model_name="alert",
            index=django.contrib.postgres.indexes.GinIndex(fields=["operator"], name="alert_operator_gin"),
        ),
        migrations.AddIndex(
            model_name="alertremindertask",
            index=models.Index(fields=["is_active", "next_reminder_time"], name="alerts_remi_is_acti_33c4e2_idx"),
        ),
    ]

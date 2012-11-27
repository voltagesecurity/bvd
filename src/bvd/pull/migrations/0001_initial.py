# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CiServer'
        db.create_table('pull_ciserver', (
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
        ))
        db.send_create_signal('pull', ['CiServer'])

        # Adding model 'CiJob'
        db.create_table('pull_cijob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ci_server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pull.CiServer'])),
            ('jobname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('pull', ['CiJob'])

        # Adding model 'UserCiJob'
        db.create_table('pull_usercijob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ci_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pull.CiJob'])),
            ('displayname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('left', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('top', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('readonly', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('entity_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pull', ['UserCiJob'])


    def backwards(self, orm):
        # Deleting model 'CiServer'
        db.delete_table('pull_ciserver')

        # Deleting model 'CiJob'
        db.delete_table('pull_cijob')

        # Deleting model 'UserCiJob'
        db.delete_table('pull_usercijob')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'pull.cijob': {
            'Meta': {'object_name': 'CiJob'},
            'ci_server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pull.CiServer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'pull.ciserver': {
            'Meta': {'object_name': 'CiServer'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'})
        },
        'pull.usercijob': {
            'Meta': {'object_name': 'UserCiJob'},
            'ci_job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pull.CiJob']"}),
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'entity_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'readonly': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'top': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pull']
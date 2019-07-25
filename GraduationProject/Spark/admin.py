from django.contrib import admin
from Spark.models import MovieInfo as MI
from Spark.models import UserRec as UR
from Spark.models import User as UI
from Spark.models import HistoricalData as HD
from Spark.models import ItemRec as IR
# Register your models here.


class movie_info_admin(admin.ModelAdmin):
	list_display = ('movie_id', 'movie_title', 'movie_type', 'movie_ctr', 'movie_lan', 'movie_date', 'movie_time', 'movie_intro', 'movie_pic', 'movie_dir', 'movie_big_pic',)
	search_fields = ('movie_id', 'movie_title', 'movie_type', 'movie_ctr', 'movie_lan', 'movie_time',)

class user_rec_admin(admin.ModelAdmin):
	list_display = ('user_id', 'user_rec',)
	search_fields = ('user_id',)

class user_info_admin(admin.ModelAdmin):
	list_display = ('user_id', 'email',)
	search_fileds = ('usr_id', )

class historical_data_admin(admin.ModelAdmin):
	list_display = ('user_id', 'movie_id', 'ratings', 'timestamp',)
	search_fields = ('user_id',)

class item_rec_admin(admin.ModelAdmin):
	list_display = ('movie_id', 'item_rec',)
	search_fields = ('movie_id',)

admin.site.register(UR, user_rec_admin)
admin.site.register(MI, movie_info_admin)
admin.site.register(UI, user_info_admin)
admin.site.register(HD, historical_data_admin)
admin.site.register(IR, item_rec_admin)

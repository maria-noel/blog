@servers(['blog-digital-ocean' => 'serial-macevedo'])

@task('list', ['on' => 'blog-digital-ocean'])
	cd /var/www/blog
	git pull origin master
	composer install
	
	sudo /usr/sbin/service php7.2-fpm restart
@endtask

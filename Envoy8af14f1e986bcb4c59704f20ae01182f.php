<?php $__container->servers(['blog-digital-ocean' => 'serial-macevedo']); ?>;

<?php $__container->startTask(['list', ['on' => 'blog-digital-ocean']); ?>
	cd /var/www/blog
	git pull origin master
	composer install
<?php $__container->endTask(); ?>
